from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("gallery", "0002_material_image"),
        ("users", "0001_userprofile"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="userprofile",
            name="phone",
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.CreateModel(
            name="OrderRequest",
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
                ("width", models.PositiveIntegerField(verbose_name="Ширина (мм)")),
                ("height", models.PositiveIntegerField(verbose_name="Высота (мм)")),
                ("quantity", models.PositiveIntegerField(verbose_name="Количество")),
                (
                    "total_price",
                    models.DecimalField(
                        decimal_places=2,
                        max_digits=14,
                        verbose_name="Стоимость по расчёту",
                    ),
                ),
                ("phone", models.CharField(max_length=20, verbose_name="Телефон")),
                ("address", models.CharField(max_length=255, verbose_name="Адрес")),
                ("comment", models.TextField(blank=True, verbose_name="Комментарий")),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("new", "Новая заявка"),
                            ("processing", "В обработке"),
                            ("confirmed", "Подтверждена"),
                            ("completed", "Завершена"),
                            ("cancelled", "Отменена"),
                        ],
                        default="new",
                        max_length=20,
                        verbose_name="Статус",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="Дата заявки")),
                (
                    "material",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="order_requests",
                        to="gallery.materials",
                        verbose_name="Материал",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="order_requests",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Пользователь",
                    ),
                ),
            ],
            options={
                "verbose_name": "Заявка на заказ",
                "verbose_name_plural": "Заявки на заказ",
                "ordering": ["-created_at"],
            },
        ),
    ]
