from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile",
    )
    avatar = models.ImageField(
        upload_to="avatars/%Y/%m/%d/",
        blank=True,
        null=True,
    )
    region = models.CharField(max_length=100, blank=True)
    address = models.CharField(max_length=255, blank=True)
    phone = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return f"Профиль {self.user.username}"


class OrderRequest(models.Model):
    STATUS_CHOICES = [
        ("new", "Новая заявка"),
        ("processing", "В обработке"),
        ("confirmed", "Подтверждена"),
        ("completed", "Завершена"),
        ("cancelled", "Отменена"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="order_requests",
        verbose_name="Пользователь",
    )
    material = models.ForeignKey(
        "gallery.Materials",
        on_delete=models.PROTECT,
        related_name="order_requests",
        verbose_name="Материал",
    )
    width = models.PositiveIntegerField("Ширина (мм)")
    height = models.PositiveIntegerField("Высота (мм)")
    quantity = models.PositiveIntegerField("Количество")
    total_price = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        verbose_name="Стоимость по расчёту",
    )
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    address = models.CharField(max_length=255, verbose_name="Адрес")
    comment = models.TextField(blank=True, verbose_name="Комментарий")
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="new",
        verbose_name="Статус",
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата заявки")

    class Meta:
        verbose_name = "Заявка на заказ"
        verbose_name_plural = "Заявки на заказ"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Заявка №{self.pk} — {self.user.username}"
