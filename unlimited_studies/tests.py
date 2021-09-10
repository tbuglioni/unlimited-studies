from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse


User = get_user_model()


class UserTestCase(TestCase):
    def test_legal_page_exists(self):
        response = self.client.get(reverse('legal'))
        self.assertEqual(response.status_code, 200)
