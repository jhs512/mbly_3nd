from django.test import TestCase

# Create your tests here.
from accounts.models import User


class AccountsTests(TestCase):
    def test_create_user(self):
        user: User = User.objects.create_user(username='admin', password='admin', name='홍길동', email='test@test.com')
        self.assertTrue(user.username == 'admin')
