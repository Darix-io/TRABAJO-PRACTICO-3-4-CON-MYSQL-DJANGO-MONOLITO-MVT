from django.contrib import admin
from django.test import TestCase

from .models import Usuario


class UsuarioAdminTests(TestCase):
    def test_usuario_is_registered_in_admin(self):
        self.assertIn(Usuario, admin.site._registry)
