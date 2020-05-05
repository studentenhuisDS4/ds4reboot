from datetime import timedelta

from django.contrib.auth.models import User
from django.template import Context, Template
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from django.utils.datetime_safe import datetime

from ds4reboot.tests import assert_total_balance
from eetlijst.models import Dinner, UserDinner
from eetlijst.urls import urlpatterns
from rainbowtests import colors
# Create your tests here.
from user.models import Housemate
from django.core.exceptions import ObjectDoesNotExist


class DinnerTest(TestCase):
    skip_nonstatic = ['enroll', 'close', 'cost', 'goto date', 'ho', 'transfer']
    dinner_enroll_url = reverse('enroll')
    dinner_close_url = reverse('close')
    dinner_cost_url = reverse('cost')
    remove_housemate_url = reverse('remove housemate')

    def setUp(self):
        print("[Testing EETLIJST]:")
        self.createHouseAccount()

        self.user = User.objects.create_superuser(
            'pietje', 'studentenhuisds4@gmail.com', 'PietjePuk')
        self.user2 = User.objects.create_superuser(
            'pietje2', 'studentenhuisds5@gmail.com', 'Pietje2Puk2')
        self.hm_pietje = Housemate.objects.create(user=User.objects.get(username='pietje'), display_name='PietjePuk',
                                                  balance=-2)
        self.hm_pietje2 = Housemate.objects.create(user=User.objects.get(username='pietje2'),
                                                   display_name='Pietje2Puk2', balance=2)

        self.assertIsNotNone(self.dinner_enroll_url)
        self.assertIsNotNone(self.dinner_close_url)
        self.assertIsNotNone(self.dinner_cost_url)
    
    def createHouseAccount(self):
        User.objects.create_superuser(
            'huis', 'studentenhuisds4@gmail.com', 'Studentenhuis')
        Housemate.objects.create(user=User.objects.get(
            username='huis'), display_name='Huis')
    
    def removeHouseAccount(self):
        User.objects.filter(username='huis').delete()
        Housemate.objects.filter(display_name='Huis').delete()

    def tearDown(self):
        User.objects.filter(username='pietje').delete()
        User.objects.filter(username='pietje2').delete()
        User.objects.filter(username='huis').delete()
        Dinner.objects.all().delete()
        UserDinner.objects.all().delete()

    def test_static_responses(self):
        for url in urlpatterns:
            if url.name not in self.skip_nonstatic and url.name is not None:
                response = self.client.get(reverse(url.name), follow=True)
                self.assertEqual(response.status_code, 200, msg=str(response))

    def test_eetlijst_without_houseuser(self):
        self.removeHouseAccount()

        print("- Testing eetlijst without house account")
        response = self.client.get(reverse('eetlijst index'))
        self.assertEqual(response.status_code, 200)

        # Make other tests runnable again
        self.createHouseAccount()

    def test_closing_dinner(self):
        print("- Testing dinner with 2 housemates subbed on dinner")
        week_ago = datetime.now() - timedelta(days=7)
        assert_total_balance()
        dinner = Dinner.objects.create(date=week_ago)
        dinner.save()

        logged_in = self.client.login(username='pietje', password='PietjePuk')
        print(colors.yellow("Loggin in user for authenticated parts: "),
              colors.blue(logged_in))
        self.assertTrue(logged_in)

        data = {
            'enroll_date': week_ago.date(),
            'enroll_type': 'signup',
            'user_id': self.user2.id
        }
        response = self.client.post(self.dinner_enroll_url, data, follow=False)
        self.assertEqual(response.status_code, 200)

        data2 = {
            'enroll_date': week_ago.date(),
            'enroll_type': 'cook',
            'user_id': self.user.id
        }
        response = self.client.post(
            self.dinner_enroll_url, data2, follow=False)
        self.assertEqual(response.status_code, 200)

        print(colors.yellow("Closing dinner date: "),
              colors.blue(timezone.now().date()))
        data = {
            'close-date': week_ago.date(),
        }
        response = self.client.post(
            self.dinner_close_url, data, follow=True, HTTP_REFERER='/eetlijst/')
        self.assertEqual(response.status_code, 200)

        data3 = {
            'cost-date': week_ago.date(),
            'cost-amount': 15
        }
        response = self.client.post(
            self.dinner_cost_url, data3, follow=True, HTTP_REFERER='/eetlijst/')
        print(colors.yellow("Filled in costs."))


class BalanceColorTagTest(TestCase):
    """ This is a tryout for learning purposes """

    TEMPLATE = Template("{% load balance_color %} {{ 32.14|bal_color }}")
    TEMPLATE2 = Template("{% load balance_color %} {{ 15.48|bal_color }}")

    # Create housemate user
    def setUp(self):
        print("[Dummy test]")
        User.objects.filter(username='huis').delete()
        User.objects.create_superuser(
            'huis', 'studentenhuisds4@gmail.com', 'Studentenhuis')
        Housemate.objects.create(user=User.objects.get(
            username='huis'), display_name='Huis')

    def tearDown(self):
        User.objects.filter(username='huis').delete()

    def test_entry_shows_up(self):
        rendered = self.TEMPLATE.render(Context({}))
        rendered2 = self.TEMPLATE2.render(Context({}))

        self.assertIn("110, 185, 110, 0.85", rendered)
        self.assertIn("180, 218, 180, 0.85", rendered2)

    skip_nonstatic = ['goto date', 'enroll', 'close', 'cost', 'ho', 'transfer']

    def test_static_responses(self):
        for url in urlpatterns:
            if url.name not in self.skip_nonstatic and url.name is not None:
                response = self.client.get(reverse(url.name), follow=True)
                self.assertEqual(response.status_code, 200)
