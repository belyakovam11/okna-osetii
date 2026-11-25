from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="HomePageAppearance",
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
                (
                    "background_image",
                    models.ImageField(
                        blank=True,
                        help_text="Необязательно. Если не указано, останется иллюстрация гор.",
                        upload_to="site/",
                        verbose_name="Фоновое изображение главной страницы",
                    ),
                ),
            ],
            options={
                "verbose_name": "Оформление главной страницы",
                "verbose_name_plural": "Оформление главной страницы",
            },
        ),
    ]
