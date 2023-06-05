from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    user = models.ForeignKey(User, blank=False, on_delete=models.CASCADE)
    telegram_user_id = models.IntegerField(blank=False)
    phoneNumber = models.CharField(null=True, max_length=9, unique=True)


    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'


class Category(models.Model):
    name = models.CharField(max_length=200, db_index=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Product(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', verbose_name='Категория')
    name = models.CharField(max_length=200, db_index=True, verbose_name='Название товара')
    description = models.TextField(blank=True, verbose_name='Описание товара')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Стоимость')
    image = models.ImageField(upload_to='tgbot_ema/images', verbose_name='Фото товара')

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return f' {self.name}, {self.price}, {self.description}, {self.image}'









