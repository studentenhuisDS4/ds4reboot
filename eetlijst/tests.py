from django.contrib.auth.models import User
from django.template import Template, Context
from django.test import TestCase
from django.urls import reverse

from eetlijst.urls import urlpatterns

# Create your tests here.
from user.models import Housemate


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
