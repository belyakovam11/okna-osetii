from django.test import TestCase
from django.urls import reverse

from .models import CompletedWork, CustomerReview, HomePageAppearance


class HomePageAppearanceTests(TestCase):
    def test_homepage_uses_the_mountain_illustration_without_custom_background(self):
        response = self.client.get(reverse("home"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'class="mountains"')
        self.assertContains(response, 'class="window__ornament"')

    def test_homepage_uses_uploaded_background_image(self):
        HomePageAppearance.objects.create(
            background_image="site/ossetian-landscape.jpg",
        )

        response = self.client.get(reverse("home"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            '<img class="hero__background-image" src="/media/site/ossetian-landscape.jpg" alt="">',
        )
        self.assertNotContains(response, 'class="mountains"')


class ReviewsAndWorksTests(TestCase):
    def test_customer_review_is_hidden_until_approved(self):
        response = self.client.post(
            reverse("reviews_and_works"),
            {
                "author_name": "Алина",
                "rating": "5",
                "text": "Отличный монтаж и очень тёплые окна!",
                "website": "",
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response["Location"], reverse("reviews_and_works"))
        review = CustomerReview.objects.get(author_name="Алина")
        self.assertFalse(review.is_published)

        page = self.client.get(reverse("reviews_and_works"))
        self.assertNotContains(page, "Отличный монтаж и очень тёплые окна!")
        self.assertContains(page, "появится на сайте после проверки")

    def test_only_approved_reviews_and_published_work_are_visible(self):
        CustomerReview.objects.create(
            author_name="Мария",
            rating=5,
            text="Работой довольны, всё сделали аккуратно.",
            is_published=True,
        )
        CompletedWork.objects.create(
            title="Окна в загородном доме",
            description="Установили окна с видом на горы.",
            image="projects/house.jpg",
            location="Владикавказ",
            is_published=True,
        )
        CompletedWork.objects.create(
            title="Скрытый проект",
            description="Пока не готов к публикации.",
            image="projects/draft.jpg",
            is_published=False,
        )

        response = self.client.get(reverse("reviews_and_works"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Работой довольны, всё сделали аккуратно.")
        self.assertContains(response, "Окна в загородном доме")
        self.assertNotContains(response, "Скрытый проект")

    def test_invalid_review_is_not_saved(self):
        response = self.client.post(
            reverse("reviews_and_works"),
            {
                "author_name": "Гость",
                "rating": "9",
                "text": "Коротко",
                "website": "",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(CustomerReview.objects.count(), 0)
        self.assertContains(response, "Напишите отзыв не короче 10 символов.")
