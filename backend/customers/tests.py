from django.test import RequestFactory, TestCase

from .models import Cliente
from .views import ClienteUpdateView


class ClienteUpdateViewTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_update_view_can_access_soft_deleted_client(self):
        cliente = Cliente.all_objects.create(
            cedula='1234567890',
            nombre='Ana Pérez',
            email='ana@example.com',
        )
        cliente.soft_delete()

        view = ClienteUpdateView()
        view.request = self.factory.get('/')

        queryset = view.get_queryset()

        self.assertIn(cliente, queryset)
