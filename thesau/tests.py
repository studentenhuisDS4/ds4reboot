from datetime import timedelta
from decimal import Decimal

from django.contrib.auth.models import User
from django.db import connection
from django.db.models import Sum
from django.test import TestCase, Client

# Create your tests here.
from django.urls import reverse
from django.utils.datetime_safe import datetime
from rainbowtests import colors

import eetlijst
from eetlijst.models import DateList, UserList
from thesau.models import Report, BoetesReport
from thesau.urls import urlpatterns
from user.models import Housemate


class ThesauTest(TestCase):
    skip_nonstatic = ['hr report', 'submit hr']
    dinner_close_url = reverse('close')
    dinner_cost_url = reverse('cost')
    remove_housemate_url = reverse('remove housemate')
    hr_url = reverse('submit hr')

    def setUp(self):
        print(">> SETUP: Refreshing user huis, adding two custom users")
        User.objects.filter(username='huis').delete()
        User.objects.create_superuser('huis', 'studentenhuisds4@gmail.com', 'Studentenhuis')
        Housemate.objects.create(user=User.objects.get(username='huis'), display_name='Huis')

        self.user = User.objects.create_superuser('pietje', 'studentenhuisds4@gmail.com', 'PietjePuk')
        self.user2 = User.objects.create_superuser('pietje2', 'studentenhuisds5@gmail.com', 'Pietje2Puk2')
        self.user3 = User.objects.create_superuser('pietje3', 'studentenhuisds6@gmail.com', 'Pietje3Puk3')
        self.hm_pietje = Housemate.objects.create(user=User.objects.get(username='pietje'), display_name='PietjePuk',
                                                  balance=-2)
        self.hm_pietje2 = Housemate.objects.create(user=User.objects.get(username='pietje2'),
                                                   display_name='Pietje2Puk2', balance=1)
        self.hm_pietje3 = Housemate.objects.create(user=User.objects.get(username='pietje3'),
                                                   display_name='Pietje3Puk3', balance=1)

        self.assertIsNotNone(self.dinner_close_url)
        self.assertIsNotNone(self.dinner_cost_url)

        self.report = Report.objects.create(report_user=self.user, report_name="TEST REPORT")
        self.bwijn_w = BoetesReport.objects.create(type='w')
        self.bwijn_r = BoetesReport.objects.create(type='r')

    def tearDown(self):
        print(">> TEARDOWN: Delete user huis")
        User.objects.filter(username='pietje').delete()

    def test_static_responses(self):
        print("Testing Thesau:")
        for url in urlpatterns:
            print("- " + str(url.name))
            if url.name not in self.skip_nonstatic and url.name is not None:
                response = self.client.get(reverse(url.name), follow=True)
                print(str(response))
                self.assertEqual(response.status_code, 200)
            else:
                print("-- url POST skipped --")

    def test_closing_hr(self):
        print("Testing closing HR with old housemate on dinner day")
        self.assert_total_balance()
        week_ago = datetime.now() - timedelta(days=7)

        # add users (normal, cook) to dinner entries
        dinnerpietje = UserList.objects.create(list_date=week_ago, user=self.user)
        dinnerpietje.list_cook = True
        dinnerpietje.save()

        dinnerpietje2 = UserList.objects.create(list_date=week_ago, user=self.user2)
        dinnerpietje2.list_count = 1
        dinnerpietje2.save()

        # add cook to date
        date = DateList.objects.create(date=week_ago)
        date.cook = self.user
        date.num_eating = 2
        date.save()

        logged_in = self.client.login(username='pietje', password='PietjePuk')
        print(colors.yellow("Loggin in user for authenticated parts: "), colors.blue(logged_in))
        self.assertTrue(logged_in)

        print(colors.yellow("Closing dinner date: "), colors.blue(datetime.now().date()))
        data = {
            'close-date': week_ago.date(),
        }
        response = self.client.post(self.dinner_close_url, data, follow=True, HTTP_REFERER='/eetlijst/')
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

        date.refresh_from_db()
        self.assertFalse(date.open, "The dinner date was not closed!")
        print(colors.yellow("Dinner closed: "), colors.blue(str(not date.open)))

        data2 = {
            'housemate': self.hm_pietje2.id,
        }
        response = self.client.post(self.remove_housemate_url, data2, follow=True, HTTP_REFERER='/thesau/')
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)
        self.hm_pietje2.refresh_from_db()
        self.assertIsNone(self.hm_pietje2.moveout_date)
        print(colors.blue("Housemate pietje2 not removed because of open dinners (move-out date): "),
              colors.blue(str(self.hm_pietje2.moveout_date)))

        data3 = {
            'cost-date': week_ago.date(),
            'cost-amount': 15
        }
        response = self.client.post(self.dinner_cost_url, data3, follow=True, HTTP_REFERER='/eetlijst/')
        print(colors.yellow("Filled in costs."))
        self.assert_total_balance()

        print(colors.yellow("Submitting HR"))
        response = self.client.post(self.hr_url, follow=True, HTTP_REFERER='/thesau/')
        self.assert_total_balance()

        data2 = {
            'housemate': self.hm_pietje2.id,
        }
        response = self.client.post(self.remove_housemate_url, data2, follow=True, HTTP_REFERER='/thesau/')
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)
        self.hm_pietje2.refresh_from_db()
        self.assertIsNotNone(self.hm_pietje2.moveout_date)
        print(colors.blue("Housemate pietje2 now correctly removed (move-out date): "),
              colors.blue(str(self.hm_pietje2.moveout_date)))
        self.assert_total_balance()

    def assert_total_balance(self):
        total_bal = Housemate.objects.filter(user__is_active=True).aggregate(Sum('balance'))['balance__sum']
        self.assertEqual(total_bal, 0)
        print(colors.cyan("Balance correct: "), colors.blue(str(total_bal)))