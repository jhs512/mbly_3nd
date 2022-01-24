from django.test import TestCase

# Create your tests here.
from accounts.models import User


class AccountsTests(TestCase):
    def test_create_user(self):
        user: User = User.objects.create_user(username='user9', password='user9', name='홍길동', email='test@test.com')
        self.assertTrue(user.username == 'user9')
