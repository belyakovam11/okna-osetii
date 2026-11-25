from django.db import models


class Materials(models.Model):
    slug = models.SlugField(unique=True, verbose_name="URL-идентификатор")
    name = models.CharField(max_length=30, unique=True, verbose_name="Материал")
    image = models.ImageField(
        upload_to="materials/",
        blank=True,
        verbose_name="Изображение материала",
        help_text="Необязательно. Показывается при выборе материала в калькуляторе.",
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Цена за м² (₽)",
        help_text="Демонстрационный тариф. Укажите актуальную цену для точного расчёта.",
    )
    rub = models.CharField(max_length=30, default="₽", verbose_name="Валюта")
    in_stock = models.CharField(max_length=10, verbose_name="Наличие")

    class Meta:
        verbose_name = "Материал окна"
        verbose_name_plural = "Материалы окон"
        ordering = ["price", "name"]

    def __str__(self):
        return self.name