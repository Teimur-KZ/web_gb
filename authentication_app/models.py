from django.db import models
# Create your models here.
from django.contrib.auth.models import User

'''Модель профиля пользователя'''
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, blank=True) # имя пользователя
    last_name = models.CharField(max_length=100, blank=True) # фамилия пользователя
    avatar = models.ImageField(upload_to='avatars/', default='avatars/default.png') # изображение профиля, если фото не загружено, используется изображение по умолчанию
    date_of_birth = models.DateField(null=True, blank=True) # дата рождения пользователя
    adress_of_delivery_line_1 = models.CharField(max_length=100, blank=True) # адрес доставки пользователя
    adress_of_delivery_line_2 = models.CharField(max_length=100, blank=True) # адрес доставки пользователя
    adress_of_city = models.CharField(max_length=100, blank=True) # город доставки пользователя
    adress_of_state = models.CharField(max_length=100, blank=True) # область доставки пользователя
    adress_of_zip = models.CharField(max_length=10, blank=True) # индекс доставки пользователя
    phone_number = models.CharField(max_length=20, blank=True) # телефон пользователя +7(999)999-99-99 blank=True - поле не обязательное
    email_customer = models.EmailField(max_length=100, blank=False) # электронная почта пользователя, если обязательно к заполнению, то blank=False, уникальное поле unique=True
    is_active = models.BooleanField(default=True) # активен ли профиль пользователя
    is_staff = models.BooleanField(default=False) # является ли пользователь персоналом
    add_data = models.DateTimeField(auto_now_add=True) # дата добавления профиля, auto_now_add=True - дата добавляется автоматически

    def __str__(self):
        return f'Профиль пользователя {self.user.username}'


# После создания моделей необходимо выполнить миграции
# py manage.py makemigrations authentication_app
# py manage.py migrate