from django.test import TestCase
from users.models import CustomUser
# Create your tests here.

class CustomUserTestCase(TestCase):
    def setUp(self):
        CustomUser.objects.create(username = 'testuser', first_name = 'test', last_name = 'user', email = 'testuser@gmail.com',password = 'test@123')
        
    def test_user_created(self):
        self.assertEqual(CustomUser.objects.count(), 1)