from django.test import TestCase
from .models import User, Following
# Create your tests here.


class NetworkTestCase(TestCase):

    def setUp(self):

        # Create User
        u1 = User.objects.create(
            username="u1", email="u1@example.com", password="password")
        u2 = User.objects.create(
            username="u2", email="u2@example.com", password="password")

        # Followings
        f1 = Following.objects.create(user=u1, follower=u2)
        f2 = Following.objects.create(user=u1, follower=u1)

    def test_valid_following(self):
        u1 = User.objects.get(id=1)
        u2 = User.objects.get(id=2)
        f = Following.objects.get(user=u1, follower=u2)
        self.assertTrue(f.is_valid_following())

    def test_invalid_following(self):
        u1 = User.objects.get(id=1)
        f = Following.objects.get(user=u1, follower=u1)
        self.assertFalse(f.is_valid_following())
