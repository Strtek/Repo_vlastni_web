from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils import timezone
from myapp.models import CustomUser, Message

class HomeViewTests(TestCase):
    def test_view_url_exists_at_proper_location(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

class RegisterViewTests(TestCase):
    def test_view_url_exists_at_proper_location(self):
        response = self.client.get('/register/')
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/register.html')

    def test_register_user(self):
        response = self.client.post(reverse('register'), {
            'email': 'test@example.com',
            'name': 'Test User',
            'password': 'testpassword'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(CustomUser.objects.filter(username='test@example.com').exists())

class AddMessageViewTests(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username='testuser', password='12345')

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('add_message'))
        self.assertRedirects(response, '/accounts/login/?next=/add_message/')

    def test_logged_in_uses_correct_template(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('add_message'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'add_message.html')

    def test_add_message(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post(reverse('add_message'), {'content': 'Hello World'})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Message.objects.filter(content='Hello World', user=self.user).exists())

class MessageListViewTests(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username='testuser', password='12345')
        self.admin = CustomUser.objects.create_user(username='adminuser', password='12345', is_admin=True)
        self.message = Message.objects.create(user=self.user, content='Hello World', timestamp=timezone.now())

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('message_list'))
        self.assertRedirects(response, '/accounts/login/?next=/message_list/')

    def test_logged_in_uses_correct_template(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('message_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'message_list.html')

    def test_messages_displayed_for_user(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('message_list'))
        self.assertContains(response, 'Hello World')

    def test_admin_sees_all_messages(self):
        self.client.login(username='adminuser', password='12345')
        response = self.client.get(reverse('message_list'))
        self.assertContains(response, 'Hello World')

class NotAuthorizedViewTests(TestCase):
    def test_view_url_exists_at_proper_location(self):
        response = self.client.get('/not_authorized/')
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('not_authorized'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'not_authorized.html')

class UserLoginViewTests(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username='testuser', password='12345')

    def test_view_url_exists_at_proper_location(self):
        response = self.client.get('/accounts/login/')
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/login.html')

    def test_login_user(self):
        response = self.client.post(reverse('login'), {'username': 'testuser', 'password': '12345'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home'))