from django.test import TestCase
from django.urls import reverse

from ds4admin.urls import urlpatterns


class TestAdminPage(TestCase):
    skip_nonstatic = ['toggle group', 'activate housemate', 'deactivate housemate', 'remove housemate']

    def test_static_responses(self):
        print("Testing Admin:")
        for url in urlpatterns:
            print("- " + str(url.name))
            if url.name not in self.skip_nonstatic and url.name is not None:
                response = self.client.get(reverse(url.name), follow=True)
                print(str(response))
                self.assertEqual(response.status_code, 200)
            else:
                print("-- url POST skipped --")

    # TODO test toggle/remove
    # def 'toggle group', 'activate housemate', 'deactivate housemate', 'remove housemate'
