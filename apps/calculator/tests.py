from django.test import TestCase
from django.urls import reverse

from apps.gallery.models import Materials


class WindowPriceCalculationTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.material = Materials.objects.create(
            slug="test-pvc",
            name="Тестовый ПВХ",
            image="materials/test-pvc.jpg",
            price="5000.00",
            rub="₽",
            in_stock="Да",
        )

    def test_homepage_lists_available_materials(self):
        response = self.client.get(reverse("home"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Тестовый ПВХ")
        self.assertContains(response, 'data-material-slug="test-pvc"')
        self.assertContains(response, 'data-image="/media/materials/test-pvc.jpg"')
        self.assertContains(response, 'id="window-preview"')
        self.assertContains(response, 'id="material-preview-image"')

    def test_calculates_price_from_material_and_dimensions(self):
        response = self.client.post(
            reverse("calculate_window_price"),
            {
                "material": self.material.pk,
                "width": 1000,
                "height": 1000,
                "quantity": 2,
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                "material": "Тестовый ПВХ",
                "area": "1.0000",
                "unit_price": "5000.00",
                "quantity": 2,
                "total_price": "10000.00",
                "currency": "₽",
            },
        )

    def test_rejects_invalid_dimensions(self):
        response = self.client.post(
            reverse("calculate_window_price"),
            {
                "material": self.material.pk,
                "width": 99,
                "height": 1000,
                "quantity": 1,
            },
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn("размеры окна", response.json()["error"].lower())

    def test_rejects_unknown_material(self):
        response = self.client.post(
            reverse("calculate_window_price"),
            {"material": 9999, "width": 1000, "height": 1000, "quantity": 1},
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn("материал", response.json()["error"])
