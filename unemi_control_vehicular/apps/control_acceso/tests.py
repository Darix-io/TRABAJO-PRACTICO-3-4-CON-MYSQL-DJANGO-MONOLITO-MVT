from django.test import SimpleTestCase
from django.urls import reverse

from apps.control_acceso.services import GeneradorQRService


class HomePageTests(SimpleTestCase):
    def test_home_page_returns_200(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)


class GeneradorQRServiceTests(SimpleTestCase):
    def test_construir_nombre_archivo_usa_identificador_del_qr(self):
        nombre = GeneradorQRService.construir_nombre_archivo('HOJ-1596', 'a4e7f97f')
        self.assertEqual(nombre, 'qr_HOJ_1596_a4e7f97f.png')

    def test_extraer_token_del_contenido(self):
        token = GeneradorQRService.extraer_token_del_contenido('UNEMI-HOJ-1596-a4e7f97f', 'HOJ-1596')
        self.assertEqual(token, 'a4e7f97f')

    def test_construir_nombre_archivo_sanitiza_caracteres_invalidos(self):
        nombre = GeneradorQRService.construir_nombre_archivo('HOJ/1596 Á', 'abc/def')
        self.assertEqual(nombre, 'qr_HOJ_1596_abc_def.png')
