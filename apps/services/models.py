from django.db import models
from django.utils.text import slugify


class Service(models.Model):
    """Модель услуги компании (установка, замер, монтаж и т.д.)."""

    name = models.CharField('Название услуги', max_length=150)
    slug = models.SlugField('URL-идентификатор', max_length=150, unique=True, blank=True)
    short_description = models.CharField('Краткое описание', max_length=255, blank=True)
    description = models.TextField('Полное описание', blank=True)
    price = models.DecimalField(
        'Цена', max_digits=10, decimal_places=2,
        null=True, blank=True,
        help_text='Оставьте пустым, если цена рассчитывается индивидуально'
    )
    image = models.ImageField('Изображение', upload_to='services/', blank=True, null=True)
    is_active = models.BooleanField('Активна', default=True)
    order = models.PositiveIntegerField('Порядок вывода', default=0)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)

    class Meta:
        verbose_name = 'Услуга'
        verbose_name_plural = 'Услуги'
        ordering = ['order', 'name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Автоматическая генерация slug из name, если он не задан
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)

