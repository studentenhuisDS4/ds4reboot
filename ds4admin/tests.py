from django.test import TestCase
from django.urls import reverse

from ds4admin.urls import urlpatterns


class TestAdminPage(TestCase):
    skip_nonstatic = ['toggle group', 'activate housemate', 'deactivate housemate', 'remove housemate', 'create user post']

    def test_static_responses(self):
        for url in urlpatterns:
            if url.name not in self.skip_nonstatic and url.name is not None:
                response = self.client.get(reverse(url.name), follow=True)
                self.assertEqual(response.status_code, 200)
