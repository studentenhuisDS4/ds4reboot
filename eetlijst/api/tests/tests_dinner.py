from django.contrib.auth.models import User
from django.test import TestCase

from user.models import Housemate


# class DinnerTest(TestCase):
#     def setUp(self):
#         print(">> SETUP: Refreshing user huis, adding two custom users")
#         User.objects.create_superuser('huis', 'studentenhuisds4@gmail.com', 'Studentenhuis')
#         Housemate.objects.create(user=User.objects.get(username='huis'), display_name='Huis')
#
#         self.login = ('pietje', 'PietjePuk')
#         self.pietje = User.objects.create_superuser(self.login[0], 'studentenhuisds4@gmail.com', self.login[1])
#         self.pietje2 = User.objects.create_superuser('pietje2', 'studentenhuisds5@gmail.com', 'Pietje2Puk2')
#
#     def tearDown(self) -> None:
#         pass
#
#     def signup(self):
#         logged_in = self.client.login(username='pietje', password='PietjePuk')
#
