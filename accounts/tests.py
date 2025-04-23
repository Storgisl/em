from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from ads.models import Ad

User = get_user_model()


class AuthViewsTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.login_url = reverse('login')
        self.logout_url = reverse('logout')

    def test_login_view_get(self):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')

    def test_login_view_post_success(self):
        response = self.client.post(
            self.login_url,
            {'username': 'testuser', 'password': 'testpass123'}
        )
        self.assertEqual(response.status_code, 302)

    def test_logout_view(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(self.logout_url)
        self.assertEqual(response.status_code, 302)


class AdViewsTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.ad = Ad.objects.create(
            user=self.user,
            title='Test Ad',
            description='Test description',
            condition='new'
        )
        self.ad_form_url = reverse('ad_edit', kwargs={'pk': self.ad.pk})

    def test_ad_update_view_get(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(self.ad_form_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'ad_edit.html')

    def test_ad_views_require_login(self):
        response = self.client.get(self.ad_form_url)
        self.assertEqual(response.status_code, 302)
