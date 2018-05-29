from django.contrib.auth.models import User
from django.test import TestCase, RequestFactory


# Create your tests here.
class ResourceTemplateTagTest(TestCase):

    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='david', email='davidzwa@gmail.com', password='top_secret')
        self.secure_user = User.objects.create_user(
            username='secure', email='gmail', password='top_secreter', is_staff=True)

    def test_user(self):

        # Create an instance of a GET request.
        users = User.objects.all()
        self.assertEqual(len(users), 2)
        self.assertEqual(users.filter(username='david')[0].is_staff, False)
        self.assertEqual(users.exclude(username='david')[0].is_staff, True)
        print("Tested user/staff basics.")
