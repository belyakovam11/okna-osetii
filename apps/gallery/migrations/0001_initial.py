from decimal import Decimal

from django.db import migrations, models


def add_demo_materials(apps, schema_editor):
    Materials = apps.get_model("gallery", "Materials")
    materials = [
        ("pvk", "ПВХ", Decimal("5000.00")),
        ("alyuminiy", "Алюминий", Decimal("7500.00")),
        ("derevo", "Дерево", Decimal("10000.00")),
    ]
    for slug, name, price in materials:
        Materials.objects.get_or_create(
            slug=slug,
            defaults={
                "name": name,
                "price": price,
                "rub": "₽",
                "in_stock": "Да",
            },
        )


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Materials",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "slug",
                    models.SlugField(unique=True, verbose_name="URL-идентификатор"),
                ),
                ("name", models.CharField(max_length=30, unique=True, verbose_name="Материал")),
                (
                    "price",
                    models.DecimalField(
                        decimal_places=2,
                        help_text="Демонстрационный тариф. Укажите актуальную цену для точного расчёта.",
                        max_digits=10,
                        verbose_name="Цена за м² (₽)",
                    ),
                ),
                ("rub", models.CharField(default="₽", max_length=30, verbose_name="Валюта")),
                ("in_stock", models.CharField(max_length=10, verbose_name="Наличие")),
            ],
            options={
                "verbose_name": "Материал окна",
                "verbose_name_plural": "Материалы окон",
                "ordering": ["price", "name"],
            },
        ),
        migrations.RunPython(add_demo_materials, migrations.RunPython.noop),
    ]
