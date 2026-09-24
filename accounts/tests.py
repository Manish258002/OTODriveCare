from django.contrib.auth import get_user_model
from django.test import Client, TestCase


class LoginFlowTests(TestCase):
    def test_regular_user_can_login_and_reach_home(self):
        user_model = get_user_model()
        user_model.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='StrongPass123!',
            phone='1234567890',
        )

        client = Client()
        response = client.post(
            '/accounts/login/',
            {'username': 'testuser', 'password': 'StrongPass123!'},
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.wsgi_request.user.is_authenticated)
        self.assertRedirects(response, '/', fetch_redirect_response=False)
