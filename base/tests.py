from django.contrib.auth.models import User
from django.test import TestCase, RequestFactory
from django.template import Context, Template
from django.urls import reverse

from base.urls import urlpatterns


class ResourceTemplateTagTest(TestCase):

    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='david', email='davidzwa@gmail.com', password='top_secret')

    def test_audio(self):

        # Create an instance of a GET request.
        request = self.factory.get('/', secure=False)
        context = Context({'request': request})
        templ = Template(
            '{% load resource_tags %}'
            '{% audio_url %}'
        )
        rendr = templ.render(context)
        print("Tested audio_url tag:", rendr)
        self.assertIn("http://", rendr)
        self.assertIn("/static/audio/", rendr)

    def test_get_params(self):

        # Create an instance of a GET request.
        request = self.factory.get('/', {'param1': 'value', 'param2': 'value2'}, secure=False)
        context = Context({'request': request})
        template_to_render = Template(
            '{% load resource_tags %}'
            '{% get_params_url %}'
        )
        rendr = template_to_render.render(context)
        print("Tested get_params tag:", rendr)
        test_str = "param1=value"
        test_str2 = "param2=value2"
        self.assertIn(test_str, rendr)
        self.assertIn(test_str2, rendr)
        self.assertIn('/?', rendr)
        self.assertNotIn('http://', rendr)

    def test_full_static(self):
        # Create an instance of a GET request.
        request = self.factory.get('/', secure=False)
        context = Context({'request': request})
        template_to_render = Template(
            '{% load resource_tags %}'
            '{% full_static_url %}'
        )
        templ = template_to_render.render(context)
        print("Tested full_static tag:", templ)
        self.assertIn('/static/', templ)
        self.assertIn('http://', templ)

    def test_full_media(self):

        # Create an instance of a GET request.
        request = self.factory.get('/', secure=False)
        context = Context({'request': request})
        template_to_render = Template(
            '{% load resource_tags %}'
            '{% full_media_url %}'
        )
        templ = template_to_render.render(context)
        print("Tested full_media tag:", templ)
        self.assertIn('/media/', templ)
        self.assertIn('http://', templ)

    def test_static_secure(self):

        # Create an instance of a GET request.
        request = self.factory.get('/', secure=True)
        context = Context({'request': request})
        template_to_render = Template(
            '{% load resource_tags %}'
            '{% full_static_url %}'
        )
        templ = template_to_render.render(context)
        print("Tested [secure] full_static tag:", templ)
        self.assertIn('/static/', templ)
        self.assertIn('https://', templ)

    def test_responses(self):
        for url in urlpatterns:
            response = self.client.get(reverse(url.name))
            self.assertEqual(response.status_code, 200)
