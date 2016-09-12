from django.test import TestCase
from django.template import Template,Context
from templatetags import *

# Create your tests here.
class BalColorTagTest(TestCase):

    TEMPLATE = Template("{% load balance_color %} {{ 32.14|bal_color }}")
    TEMPLATE2 = Template("{% load balance_color %} {{ 15.48|bal_color }}")


    def test_entry_shows_up(self):
        rendered = self.TEMPLATE.render(Context({}))
        rendered2 = self.TEMPLATE2.render(Context({}))
        print rendered2

        self.assertIn("110, 185, 110, 0.85",rendered)
        self.assertIn("180, 219, 180, 0.85", rendered2)