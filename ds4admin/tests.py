from django.test import TestCase
from django.urls import reverse

from ds4admin.urls import urlpatterns


class TestAdminPage(TestCase):

    def test_responses(self):
        for url in urlpatterns:

            if url.name is not None:
                print("- " + str(url.name))

                response = self.client.get(reverse(url.name), follow=True)
                print(response.status_code)
                self.assertEqual(response.status_code, 200)
