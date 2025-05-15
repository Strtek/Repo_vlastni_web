from django.test import TestCase
from myapp.models import CustomUser, Message

class CustomUserTest(TestCase):
    def test_string_representation(self):
        user = CustomUser(username="testuser")
        self.assertEqual(str(user), "testuser")

    def test_is_admin_default(self):
        user = CustomUser(username="testuser")
        self.assertFalse(user.is_admin)

class MessageTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username='testuser', password='12345')

    def test_string_representation(self):
        message = Message(user=self.user, content="Hello World")
        self.assertEqual(str(message), "Message from testuser: Hello World")

    def test_message_creation(self):
        message = Message.objects.create(user=self.user, content="Hello World")
        self.assertEqual(message.content, "Hello World")
        self.assertEqual(message.user, self.user)
