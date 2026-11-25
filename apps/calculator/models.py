from django.db import models


from apps.catalog.models import ProfileSystem, WindowType, GlassUnit

class Calculation(models.Model):
    profile = models.ForeignKey(ProfileSystem, on_delete=models.SET_NULL, null=True)
    window_type = models.ForeignKey(WindowType, on_delete=models.SET_NULL, null=True)
    glass = models.ForeignKey(GlassUnit, on_delete=models.SET_NULL, null=True)
    width = models.PositiveIntegerField('Ширина (мм)')
    height = models.PositiveIntegerField('Высота (мм)')
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Расчёт {self.id}'


class Lead(models.Model):
    STATUS_CHOICES = [
        ('new', 'Новая'),
        ('measuring', 'Замер'),
        ('contract', 'Договор'),
        ('production', 'Производство'),
        ('installation', 'Монтаж'),
        ('done', 'Завершено'),
        ('cancelled', 'Отменено'),
    ]

    name = models.CharField('Имя', max_length=100)
    phone = models.CharField('Телефон', max_length=20)
    address = models.CharField('Адрес', max_length=255, blank=True)
    comment = models.TextField(blank=True)
    calculation = models.ForeignKey(Calculation, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.name} — {self.phone}'

