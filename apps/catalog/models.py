
from django.db import models

class ProfileSystem(models.Model):
    name = models.CharField('Профиль', max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='profiles/', blank=True)

    def __str__(self):
        return self.name


class WindowType(models.Model):
    name = models.CharField('Тип окна', max_length=100)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class GlassUnit(models.Model):
    name = models.CharField('Стеклопакет', max_length=100)
    thickness = models.CharField('Толщина', max_length=50)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name
