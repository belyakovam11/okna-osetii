from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0001_home_page_appearance"),
    ]

    operations = [
        migrations.CreateModel(
            name="CompletedWork",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=120, verbose_name="Название проекта")),
                ("description", models.TextField(verbose_name="Описание")),
                (
                    "image",
                    models.ImageField(
                        upload_to="projects/%Y/%m/",
                        verbose_name="Фотография готовой работы",
                    ),
                ),
                (
                    "location",
                    models.CharField(
                        blank=True,
                        max_length=100,
                        verbose_name="Город или район",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="Добавлено")),
                ("is_published", models.BooleanField(default=True, verbose_name="Опубликовано")),
            ],
            options={
                "verbose_name": "Готовая работа",
                "verbose_name_plural": "Готовые работы",
                "ordering": ["-created_at"],
            },
        ),
        migrations.CreateModel(
            name="CustomerReview",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("author_name", models.CharField(max_length=80, verbose_name="Имя")),
                ("text", models.TextField(verbose_name="Отзыв")),
                (
                    "rating",
                    models.PositiveSmallIntegerField(
                        choices=[(value, f"{value} из 5") for value in range(1, 6)],
                        verbose_name="Оценка",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="Отправлен")),
                (
                    "is_published",
                    models.BooleanField(default=False, verbose_name="Одобрен и опубликован"),
                ),
            ],
            options={
                "verbose_name": "Отзыв клиента",
                "verbose_name_plural": "Отзывы клиентов",
                "ordering": ["-created_at"],
            },
        ),
    ]
