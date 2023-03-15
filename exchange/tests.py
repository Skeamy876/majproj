from django.test import TestCase
from exchange.models import User, Book

# Create your tests here.

class LoginTestCase(TestCase):
    def setUp(self):
        self.credentials = {
            'username': 'testuser',
            'password': 'normaluser12345'}
        User.objects.create_user(**self.credentials)

    def test_login(self):
        response = self.client.post('/login/', self.credentials, follow=True)
        self.assertTrue(response.context['user'].is_authenticated)

    def test_login_fail(self):
        response = self.client.post('/login/', {'username': 'testuser', 'password': 'wrongpassword'}, follow=True)
        self.assertFalse(response.context['user'].is_authenticated)


class UserviewTestCase(TestCase):
    def setUp(self):
        self.credentials = {
            'username': 'testuser',
            'password': 'normaluser12345',
            'first_name': 'test',
            'last_name': 'user',
            }
        User.objects.create_user(**self.credentials)

        owner=User.objects.get(username='testuser')
        self.book={
            'title': 'testbook',
            'author': 'testauthor',
            'owner': owner
        }
        Book.objects.create(**self.book)

    def test_userview_load(self):
        response = self.client.post('/login/', self.credentials, follow=True)
        response = self.client.get('/accounts/testuser/')
        self.assertEqual(response.status_code, 200)

    def test_userview_load_fail(self):
        response = self.client.post('/login/', self.credentials, follow=True)
        response = self.client.get('/accounts/wrongtester/')
        self.assertEqual(response.status_code, 404)


    def test_contex_render_not_empty(self):
        response = self.client.post('/login/', self.credentials, follow=True)
        response = self.client.get('/accounts/testuser/')
        self.assertTrue(response.context['books'],"Context is empty")



      