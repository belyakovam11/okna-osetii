from django.db import models


class HomePageAppearance(models.Model):
    background_image = models.ImageField(
        upload_to="site/",
        blank=True,
        verbose_name="Фоновое изображение главной страницы",
        help_text="Необязательно. Если не указано, останется иллюстрация гор.",
    )

    class Meta:
        verbose_name = "Оформление главной страницы"
        verbose_name_plural = "Оформление главной страницы"

    def __str__(self):
        return "Фон главной страницы"


class CompletedWork(models.Model):
    title = models.CharField(max_length=120, verbose_name="Название проекта")
    description = models.TextField(verbose_name="Описание")
    image = models.ImageField(
        upload_to="projects/%Y/%m/",
        verbose_name="Фотография готовой работы",
    )
    location = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Город или район",
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Добавлено")
    is_published = models.BooleanField(default=True, verbose_name="Опубликовано")

    class Meta:
        verbose_name = "Готовая работа"
        verbose_name_plural = "Готовые работы"
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


class CustomerReview(models.Model):
    author_name = models.CharField(max_length=80, verbose_name="Имя")
    text = models.TextField(verbose_name="Отзыв")
    rating = models.PositiveSmallIntegerField(
        choices=[(value, f"{value} из 5") for value in range(1, 6)],
        verbose_name="Оценка",
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Отправлен")
    is_published = models.BooleanField(
        default=False,
        verbose_name="Одобрен и опубликован",
    )

    class Meta:
        verbose_name = "Отзыв клиента"
        verbose_name_plural = "Отзывы клиентов"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Отзыв: {self.author_name}"
