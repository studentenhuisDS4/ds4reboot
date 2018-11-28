from django.template import Template, Context
from django.test import TestCase
from django.urls import reverse

from eetlijst.urls import urlpatterns


# Create your tests here.
class BalColorTagTest(TestCase):
    TEMPLATE = Template("{% load balance_color %} {{ 32.14|bal_color }}")
    TEMPLATE2 = Template("{% load balance_color %} {{ 15.48|bal_color }}")

    def test_entry_shows_up(self):
        rendered = self.TEMPLATE.render(Context({}))
        rendered2 = self.TEMPLATE2.render(Context({}))

        self.assertIn("110, 185, 110, 0.85", rendered)
        self.assertIn("180, 218, 180, 0.85", rendered2)

    def test_responses(self):
        for url in urlpatterns:
            response = self.client.get(reverse(url.name))
            print(response)
            self.assertEqual(response.status_code, 200)
