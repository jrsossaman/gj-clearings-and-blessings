from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Profile

# Create your tests here.

class ProfileModelTest(TestCase):

    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(username="Alice", password="testpass123")
        self.profile = Profile.objects.create(user=self.user)

    def test_profile_user_link(self):
        self.assertEqual(self.profile.user, self.user)
        self.assertEqual(self.profile.user.username, "Alice")