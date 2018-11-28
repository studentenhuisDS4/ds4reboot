from django.test import TestCase
from django.urls import reverse

from bierlijst.urls import urlpatterns


class TestBierlijst(TestCase):
    skip_nonstatic = [
        'add boetes', 'remove boetes', 'turf boetes', 'turf'
    ]

    # Test medals before anything else, because medals by javascript.
    def test_medals(self):
        response = self.client.get(reverse("medals"))
        self.assertEqual(response.status_code, 200)

    def test_static_responses(self):
        print("Testing bierlijst:")
        for url in urlpatterns:
            print("- " + str(url.name))
            if url.name not in self.skip_nonstatic:
                response = self.client.get(reverse(url.name), follow=True)
                print(str(response))
                self.assertEqual(response.status_code, 200)
            else:
                print("-- url POST skipped --")

    def test_boete_post_enforced(self):
        response = self.client.get(reverse('add boetes'), follow=True)
        # Expect POST
        self.assertEqual(response.status_code, 405)

    # TODO add boetes, remove boetes, turf boetes, turf
    # def test_boetes:

    # def turf:

