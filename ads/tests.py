from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Ad
from .basefolder.choices import CategoryChoices

User = get_user_model()

class IndexViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('index')

    def test_index_view(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')


class AdEditTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.ad = Ad.objects.create(user=self.user, title='Original', description='Original')
        self.url = reverse('ad_edit', kwargs={'pk': self.ad.pk})


class AdCreateTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.url = reverse('ad_create')

    def test_ad_create_get(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'ad_create.html')
