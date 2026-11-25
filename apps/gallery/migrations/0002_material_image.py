from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("gallery", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="materials",
            name="image",
            field=models.ImageField(
                blank=True,
                help_text="Необязательно. Показывается при выборе материала в калькуляторе.",
                upload_to="materials/",
                verbose_name="Изображение материала",
            ),
        ),
    ]
