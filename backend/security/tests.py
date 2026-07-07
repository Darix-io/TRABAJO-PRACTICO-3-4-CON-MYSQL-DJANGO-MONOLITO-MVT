from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class UserListViewTests(TestCase):
    def test_users_list_view_renders_for_superuser(self):
        user = get_user_model().objects.create_superuser(
            username='admin',
            first_name='Admin',
            last_name='User',
            email='admin@example.com',
            password='12345678',
        )

        self.client.force_login(user)
        response = self.client.get(reverse('security:user_list'))

        self.assertEqual(response.status_code, 200)
