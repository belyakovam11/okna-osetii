from io import BytesIO
import tempfile

from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse
from PIL import Image

from apps.gallery.models import Materials
from .models import OrderRequest, UserProfile


class AccountFlowTests(TestCase):
    def setUp(self):
        self.registration_data = {
            "username": "window_customer",
            "email": "customer@example.com",
            "password1": "Pine!River_9516",
            "password2": "Pine!River_9516",
            "phone": "+7 (900) 123-45-67",
            "region": "Республика Северная Осетия — Алания",
            "address": "Владикавказ, улица Мира, 10",
        }

    def test_registration_creates_user_and_profile_and_logs_in(self):
        response = self.client.post(
            reverse("user_register"),
            self.registration_data,
        )

        self.assertRedirects(response, reverse("user_profile"))
        user = User.objects.get(username="window_customer")
        self.assertTrue(user.check_password("Pine!River_9516"))
        self.assertEqual(user.profile.region, self.registration_data["region"])
        self.assertEqual(user.profile.address, self.registration_data["address"])
        self.assertEqual(user.profile.phone, self.registration_data["phone"])
        self.assertIn("_auth_user_id", self.client.session)

    def test_profile_can_be_updated(self):
        self.client.post(reverse("user_register"), self.registration_data)
        user = User.objects.get(username="window_customer")

        response = self.client.post(
            reverse("user_profile"),
            {
                "email": "updated@example.com",
                "region": "Ставропольский край",
                "address": "Пятигорск, проспект Кирова, 5",
                "phone": "+7 999 123-45-67",
            },
        )

        self.assertRedirects(response, reverse("user_profile"))
        user.refresh_from_db()
        user.profile.refresh_from_db()
        self.assertEqual(user.email, "updated@example.com")
        self.assertEqual(user.profile.region, "Ставропольский край")
        self.assertEqual(user.profile.address, "Пятигорск, проспект Кирова, 5")
        self.assertEqual(user.profile.phone, "+7 999 123-45-67")

    def test_login_requires_valid_credentials(self):
        User.objects.create_user(username="customer", password="Pine!River_9516")

        invalid_response = self.client.post(
            reverse("user_login"),
            {"username": "customer", "password": "wrong-password"},
        )
        self.assertEqual(invalid_response.status_code, 200)
        self.assertNotIn("_auth_user_id", self.client.session)

        valid_response = self.client.post(
            reverse("user_login"),
            {"username": "customer", "password": "Pine!River_9516"},
        )
        self.assertRedirects(valid_response, reverse("user_profile"))
        self.assertIn("_auth_user_id", self.client.session)

    def test_api_registration_returns_auth_token_and_profile(self):
        response = self.client.post(
            reverse("api_user_register"),
            {
                "username": "api_customer",
                "password": "Pine!River_9516",
                "password2": "Pine!River_9516",
                "profile": {
                    "region": "Республика Северная Осетия — Алания",
                    "address": "Владикавказ, улица Мира, 10",
                },
            },
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 201)
        self.assertTrue(response.json()["token"])
        self.assertEqual(
            response.json()["user"]["profile"]["region"],
            "Республика Северная Осетия — Алания",
        )

    def test_api_login_returns_token_for_valid_credentials(self):
        User.objects.create_user(username="api_customer", password="Pine!River_9516")

        invalid_response = self.client.post(
            reverse("api_user_login"),
            {"username": "api_customer", "password": "wrong-password"},
            content_type="application/json",
        )
        self.assertEqual(invalid_response.status_code, 400)

        valid_response = self.client.post(
            reverse("api_user_login"),
            {"username": "api_customer", "password": "Pine!River_9516"},
            content_type="application/json",
        )
        self.assertEqual(valid_response.status_code, 200)
        self.assertTrue(valid_response.json()["token"])

    def test_registration_accepts_avatar_upload(self):
        image_buffer = BytesIO()
        Image.new("RGB", (1, 1), color="green").save(image_buffer, format="PNG")

        with tempfile.TemporaryDirectory() as media_root:
            with override_settings(MEDIA_ROOT=media_root):
                response = self.client.post(
                    reverse("user_register"),
                    {
                        **self.registration_data,
                        "avatar": SimpleUploadedFile(
                            "avatar.png",
                            image_buffer.getvalue(),
                            content_type="image/png",
                        ),
                    },
                )

                self.assertRedirects(response, reverse("user_profile"))
                profile = UserProfile.objects.get(user__username="window_customer")
                self.assertTrue(profile.avatar.storage.exists(profile.avatar.name))

    def test_customer_can_submit_order_and_view_its_status(self):
        user = User.objects.create_user(username="order_customer", password="Pine!River_9516")
        UserProfile.objects.create(
            user=user,
            phone="+7 900 123-45-67",
            address="Владикавказ, улица Мира, 10",
        )
        material = Materials.objects.create(
            slug="order-test-pvc",
            name="ПВХ для заказа",
            price="5000.00",
            in_stock="Да",
        )
        self.client.force_login(user)

        response = self.client.post(
            reverse("user_profile"),
            {
                "form_type": "order",
                "material": material.pk,
                "width": 1000,
                "height": 1000,
                "quantity": 2,
                "phone": "+7 900 123-45-67",
                "address": "Владикавказ, улица Мира, 10",
                "comment": "Позвонить вечером",
            },
        )

        self.assertRedirects(response, reverse("user_profile"))
        order = OrderRequest.objects.get(user=user)
        self.assertEqual(order.total_price, 10000)
        self.assertEqual(order.status, "new")
        self.assertEqual(order.material, material)
        self.assertEqual(order.comment, "Позвонить вечером")
        self.assertContains(self.client.get(reverse("user_profile")), "Заявка №1")

    def test_customer_cannot_view_another_users_order(self):
        owner = User.objects.create_user(username="first_customer")
        other_user = User.objects.create_user(username="second_customer")
        material = Materials.objects.create(
            slug="private-order-pvc",
            name="Материал для приватной заявки",
            price="5000.00",
            in_stock="Да",
        )
        OrderRequest.objects.create(
            user=owner,
            material=material,
            width=1000,
            height=1000,
            quantity=1,
            total_price=5000,
            phone="+7 900 111-22-33",
            address="Адрес первого клиента",
        )
        self.client.force_login(other_user)

        response = self.client.get(reverse("user_profile"))

        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "Адрес первого клиента")

    def test_order_rejects_dimensions_outside_calculator_range(self):
        user = User.objects.create_user(username="invalid_order_customer")
        UserProfile.objects.create(user=user)
        material = Materials.objects.create(
            slug="invalid-order-pvc",
            name="Некорректный заказ",
            price="5000.00",
            in_stock="Да",
        )
        self.client.force_login(user)

        response = self.client.post(
            reverse("user_profile"),
            {
                "form_type": "order",
                "material": material.pk,
                "width": 99,
                "height": 1000,
                "quantity": 1,
                "phone": "+7 900 123-45-67",
                "address": "Владикавказ, улица Мира, 10",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(OrderRequest.objects.count(), 0)
        self.assertTrue(response.context["order_form"].errors["width"])
