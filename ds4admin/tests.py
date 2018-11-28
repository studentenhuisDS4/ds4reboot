from django.test import TestCase
from django.urls import reverse

from ds4admin.urls import urlpatterns


class TestAdminPage(TestCase):

    def test_responses(self):
        for url in urlpatterns:
            response = self.client.get(reverse(url.name))
            print(response)
            self.assertEqual(response.status_code, 200)
