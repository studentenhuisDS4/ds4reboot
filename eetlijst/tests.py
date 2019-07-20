from datetime import timedelta

from django.contrib.auth.models import User
from django.template import Template, Context
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from openpyxl.utils import datetime
from rainbowtests import colors

from ds4reboot.tests import assert_total_balance
from eetlijst.models import Dinner, UserDinner
from eetlijst.urls import urlpatterns

# Create your tests here.
from user.models import Housemate


### This is a tryout for learning purposes
class BalColorTagTest(TestCase):
    TEMPLATE = Template("{% load balance_color %} {{ 32.14|bal_color }}")
    TEMPLATE2 = Template("{% load balance_color %} {{ 15.48|bal_color }}")

    # Create housemate user
    def setUp(self):
        print("-! Refreshing user huis")
        User.objects.filter(username='huis').delete()
        User.objects.create_superuser('huis', 'studentenhuisds4@gmail.com', 'Studentenhuis')
        Housemate.objects.create(user=User.objects.get(username='huis'), display_name='Huis')

    def tearDown(self):
        print("-! Delete user huis")
        User.objects.filter(username='huis').delete()

    def test_entry_shows_up(self):
        rendered = self.TEMPLATE.render(Context({}))
        rendered2 = self.TEMPLATE2.render(Context({}))

        self.assertIn("110, 185, 110, 0.85", rendered)
        self.assertIn("180, 218, 180, 0.85", rendered2)

    skip_nonstatic = ['goto date', 'enroll', 'close', 'cost', 'ho', 'transfer']

    def test_static_responses(self):
        print("Testing Eetlijst:")
        for url in urlpatterns:
            print("- " + str(url.name))
            if url.name not in self.skip_nonstatic and url.name is not None:
                response = self.client.get(reverse(url.name), follow=True)
                print(str(response))
                self.assertEqual(response.status_code, 200)
            else:
                print("-- url POST skipped --")


# TODO test 'goto date'
# def test_goto_date:
# def test_enroll:
# def test_close:
# def test_cost:
class DinnerTest(TestCase):
    skip_nonstatic = ['enroll', 'close', 'cost', 'goto date', 'ho', 'transfer']
    dinner_enroll_url = reverse('enroll')
    dinner_close_url = reverse('close')
    dinner_cost_url = reverse('cost')

    def setUp(self):
        print(">> SETUP: Refreshing user huis, adding two custom users")
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

    def tearDown(self):
        print(">> TEARDOWN: Delete user huis")
        User.objects.filter(username='pietje').delete()
        User.objects.filter(username='pietje2').delete()
        User.objects.filter(username='pietje3').delete()
        User.objects.filter(username='huis').delete()
        Dinner.objects.all().delete()
        UserDinner.objects.all().delete()

    def test_static_responses(self):
        print("Testing Eetlijst:")
        for url in urlpatterns:
            print("- " + str(url.name))
            if url.name not in self.skip_nonstatic and url.name is not None:
                response = self.client.get(reverse(url.name), follow=True)
                print(str(response))
                self.assertEqual(response.status_code, 200, msg=str(response))
            else:
                print("-- url POST skipped --")

    def test_dinner_cost(self):
        print("Testing closing HR with old housemate on dinner day")

        assert_total_balance()
        week_ago = timezone.now() - timedelta(days=7)

        logged_in = self.client.login(username='pietje', password='PietjePuk')
        print(colors.yellow("Loggin in user for authenticated parts: "), colors.blue(logged_in))
        self.assertTrue(logged_in)

        data = {
            'enroll_date': week_ago.date(),
            'enroll_type': 'signup',
            'user_id': self.user2.id
        }
        print(data)
        return None
        
        response = self.client.post(self.dinner_enroll_url, data, follow=False)
        self.assertEqual(response.status_code, 200)
        print(response)

        # test_dinner = Dinner.objects.filter(date=week_ago.date()).first()
        # self.assertIsNotNone(test_dinner)
        # test_dinner = None

        data = {
            'enroll_date': week_ago.date(),
            'enroll_type': 'cook',
            'user_id': self.user.id
        }
        response = self.client.post(self.dinner_enroll_url, data, follow=True, HTTP_REFERER='/eetlijst/')
        self.assertEqual(response.status_code, 200)

        print(colors.yellow("Closing dinner date: "), colors.blue(timezone.now().date()))
        data = {
            'close-date': week_ago.date(),
        }
        response = self.client.post(self.dinner_close_url, data, follow=True, HTTP_REFERER='/eetlijst/')
        self.assertEqual(response.status_code, 200)

        # test_dinner.refresh_from_db()
        # self.assertFalse(test_dinner.open, "The dinner date was not closed!")
        # print(colors.yellow("Dinner closed: "), colors.blue(str(not test_dinner.open)))

        data3 = {
            'cost-date': week_ago.date(),
            'cost-amount': 15
        }
        response = self.client.post(self.dinner_cost_url, data3, follow=True, HTTP_REFERER='/eetlijst/')
        print(colors.yellow("Filled in costs."))
        assert_total_balance()
