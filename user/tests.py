from django.contrib.auth.models import User
from django.test import TestCase, RequestFactory

# Create your tests here.
from django.urls import reverse

from user.urls import urlpatterns


class ResourceTemplateTagTest(TestCase):

    def setUp(self):
        print("[Testing USER]:")

        # Every test needs access to the request factory.
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='david', email='davidzwa@gmail.com', password='top_secret')
        self.secure_user = User.objects.create_user(
            username='secure', email='gmail', password='top_secreter', is_staff=True)

    # def tearDown(self):
    #     print("Tested user/staff basics.")

    def test_user(self):

        # Create an instance of a GET request.
        users = User.objects.all()
        self.assertEqual(len(users), 2)
        self.assertEqual(users.filter(username='david')[0].is_staff, False)
        self.assertEqual(users.exclude(username='david')[0].is_staff, True)

    skip_nonstatic = ['logout', 'login huis']

    def test_static_responses(self):
        for url in urlpatterns:
            if url.name not in self.skip_nonstatic and url.name is not None:
                response = self.client.get(reverse(url.name), follow=True)
                self.assertEqual(response.status_code, 200)