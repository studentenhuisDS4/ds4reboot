from django.test import TestCase


# Create your tests here.
from django.urls import reverse

from thesau.urls import urlpatterns


class ThesauTest(TestCase):
    skip_nonstatic = ['hr report', 'submit hr']

    def test_static_responses(self):
        print("Testing Thesau:")
        for url in urlpatterns:
            print("- " + str(url.name))
            if url.name not in self.skip_nonstatic and url.name is not None:
                response = self.client.get(reverse(url.name), follow=True)
                print(str(response))
                self.assertEqual(response.status_code, 200)
            else:
                print("-- url POST skipped --")
