from django.db import models
from ckeditor.fields import RichTextField # импорт поля для визуального редактирования текста
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from PIL import Image

# Create your models here.

'''Модель категории товара'''

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)  # unique=True - поле name должно быть уникальным
    logo = models.ImageField(upload_to='category_logos/', blank=True, null=True)  # поле для логотипа
    description = RichTextField(blank=True, null=True)  # поле для описания
    """SEO поля"""
    seo_title = models.CharField(max_length=70, blank=True, null=True, verbose_name='SEO Заголовок', help_text='SEO Заголовок')  # SEO Заголовок
    seo_description = models.CharField(max_length=160, blank=True, null=True, verbose_name='SEO Описание', help_text='SEO Описание')  # SEO Описание
    seo_keywords = models.CharField(max_length=255, blank=True, null=True, verbose_name='SEO Ключевые слова', help_text='SEO Ключевые слова')  # SEO Ключевые слова


    def __str__(self):
        return self.name

    def save(self, *args, **kwargs): # переопределяем метод save для валидации размера логотипа
        if self.logo:
            img = Image.open(self.logo) # открываем изображение
            if img.height > 200 or img.width > 200:
                raise ValidationError("Высота и ширина логотипа не должны превышать 200 пикселей.")
        super().save(*args, **kwargs)

'''Модель Бренда'''

class Brand(models.Model):
    name = models.CharField(max_length=50, unique=True)# unique=True - поле name должно быть уникальным

    def __str__(self):
        return self.name

class ProductSize(models.Model):
    size = models.CharField(max_length=50, unique=True)# unique=True - поле size должно быть уникальным
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория размера', help_text='Выберите категорию размера') # связь многие-к-одному. on_delete=models.CASCADE - при удалении категории удалятся все размеры, связанные с ней

    class Meta:
        db_table = 'products_app_productsize'  # устанавливаем имя таблицы

    def __str__(self):
        return self.size

'''Модель товара'''

class Product(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Название товара', help_text='Введите название товара') # verbose_name - человекочитаемое имя поля, help_text - подсказка
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория товара', help_text='Выберите категорию товара') # связь многие-к-одному. on_delete=models.CASCADE - при удалении категории удалятся все продукты, связанные с ней
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, verbose_name='Бренд товара', help_text='Выберите бренд товара') # связь многие-к-одному. on_delete=models.CASCADE - при удалении бренда удалятся все продукты, связанные с ним
    description = RichTextField(verbose_name='Описание товара', help_text='Введите описание товара') # RichTextField - поле для визуального редактирования текста
    #image = models.ImageField(upload_to='products/', null=True, blank=True, verbose_name='Изображение товара', help_text='Загрузите изображение товара') # добавляем поле для изображения
    image = models.ImageField(upload_to='products/', default='products/blank.jpg', verbose_name='Изображение товара', help_text='Загрузите изображение товара') # добавляем поле для изображения
    price = models.DecimalField(default=999_999.99, max_digits=10, decimal_places=2, verbose_name='Цена товара', help_text='Введите цену товара') # max_digits=10 - максимальное количество цифр, decimal_places=2 - количество знаков после запятой
    quantity = models.PositiveSmallIntegerField(default=0, verbose_name='Количество товара', help_text='Введите количество товара') # (количество) PositiveSmallIntegerField - положительное целое число
    size = models.ManyToManyField(ProductSize, verbose_name='Размеры товара', help_text='Выберите размеры товара') # связь многие-к-одному. on_delete=models.CASCADE - при удалении размера удалятся все продукты, связанные с ним
    product_weight = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Вес товара', help_text='Введите вес товара') # вес товара
    delivery_time = models.CharField(max_length=50, verbose_name='Срок доставки', help_text='Введите срок доставки') # срок доставки
    delivery_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Стоимость доставки', help_text='Введите стоимость доставки') # стоимость доставки
    date_added = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления товара', help_text='Дата добавления товара') # auto_now_add=True - дата добавления записи (поле заполняется автоматически)
    rating = models.DecimalField(default=5.0, max_digits=3, decimal_places=2, verbose_name='Рейтинг товара', help_text='Введите рейтинг товара') # рейтинг товара (от 0 до 5)
    active = models.BooleanField(default=True, verbose_name='Активный товар', help_text='Товар активен или нет') # активен ли товар, .BooleanField() - булево значение (True/False)

    """SEO поля"""
    seo_title = models.CharField(max_length=70, blank=True, null=True, verbose_name='SEO Заголовок', help_text='SEO Заголовок')  # SEO Заголовок
    seo_description = models.CharField(max_length=160, blank=True, null=True, verbose_name='SEO Описание', help_text='SEO Описание')  # SEO Описание
    seo_keywords = models.CharField(max_length=255, blank=True, null=True, verbose_name='SEO Ключевые слова', help_text='SEO Ключевые слова')  # SEO Ключевые слова


    @staticmethod # статический метод, который возвращает список размеров
    def get_size_choices(category):
        return [(size.id, size.size) for size in ProductSize.objects.filter(category=category)]

    def __str__(self):
        return self.name

'''Модель размер и количество товара'''
class ProductSizeQuantity(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)# связь многие-к-одному. on_delete=models.CASCADE - при удалении товара удалятся все размеры и количество, связанные с ним
    size = models.ForeignKey(ProductSize, on_delete=models.CASCADE) # связь многие-к-одному. on_delete=models.CASCADE - при удалении размера удалятся все размеры и количество, связанные с ним
    quantity = models.PositiveSmallIntegerField(default=0) # (количество) PositiveSmallIntegerField - положительное целое число

    def __str__(self):
        return f"{self.product.name} (Размер: {self.size})"

'''Модель Отзыва о товаре'''

class Review(models.Model): # модель отзыва о товаре
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Товар', help_text='Выберите товар') # связь многие-к-одному. on_delete=models.CASCADE - при удалении товара удалятся все отзывы, связанные с ним
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь', help_text='Выберите пользователя') # связь многие-к-одному. on_delete=models.CASCADE - при удалении пользователя удалятся все отзывы, связанные с ним
    image = models.ImageField(upload_to='reviews/', null=True, blank=True, verbose_name='Изображение отзыва', help_text='Загрузите изображение отзыва') # добавляем поле для изображения
    text = models.TextField(verbose_name='Текст отзыва', help_text='Введите текст отзыва') # текст отзыва
    date_added = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления отзыва', help_text='Дата добавления отзыва') # auto_now_add=True - дата добавления записи (поле заполняется автоматически)
    active = models.BooleanField(default=True, verbose_name='Активный отзыв', help_text='Отзыв активен или нет') # активен ли отзыв, .BooleanField() - булево значение (True/False)

# После создания моделей необходимо выполнить миграции
# py manage.py makemigrations products_app
# py manage.py migrate
# отмена миграции
# py manage.py migrate products_app zero


