from django.db import models
from authentication_app.models import Profile
from products_app.models import Product, ProductSizeQuantity


# Create your models here.

class Order(models.Model):
    number_order = models.CharField(max_length=36, verbose_name='Номер заказа')  # номер заказа, генерируется автоматически
    user_profile = models.ForeignKey(Profile, on_delete=models.CASCADE, verbose_name='Профиль пользователя') # связь с профилем пользователя
    comment = models.TextField(verbose_name='Комментарий', blank=True) # комментарий к заказу
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания') # дата создания заказа
    updated = models.DateTimeField(auto_now=True, verbose_name='Дата обновления') # дата обновления заказа
    payment = models.ForeignKey('PaymentOptions', on_delete=models.CASCADE, verbose_name='Способ оплаты')  # способ оплаты
    paid = models.BooleanField(default=False, verbose_name='Оплачен') # оплачен ли заказ
    delivery = models.ForeignKey('DeliveryOptions', on_delete=models.CASCADE,verbose_name='Способ доставки')  # способ доставки
    delivery_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена доставки') # цена доставки
    delivery_status = models.CharField(max_length=255, verbose_name='Статус доставки') # статус доставки
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Общая цена') # общая цена заказа
    class Meta:
        ordering = ('-created',) # сортировка заказов по убыванию даты создания
    def __str__(self):
        return self.number_order

    def get_total_cost(self):
        return self.total_price + self.delivery_price


class DeliveryOptions(models.Model):
    name = models.CharField(max_length=255, verbose_name='Способ доставки')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    min_total_price_for_free_delivery = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True) #

    def __str__(self):
        return self.name


class PaymentOptions(models.Model): # модель для способов оплаты
    name = models.CharField(max_length=255, verbose_name='Способ оплаты') # название способа оплаты
    def __str__(self):
        return self.name # возвращает название способа оплаты

class OrderItemNew(models.Model):
    order = models.ForeignKey(Order, related_name='new_items', on_delete=models.CASCADE)
    product_size_quantity = models.ForeignKey(ProductSizeQuantity, related_name='new_order_items', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2) # цена товара
    quantity = models.PositiveIntegerField(default=1) # количество товара

    def get_cost(self):
        return self.price * self.quantity

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='old_items', on_delete=models.CASCADE)
    product_size_quantity = models.ForeignKey(ProductSizeQuantity, related_name='old_order_items', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2) # цена товара
    quantity = models.PositiveIntegerField(default=1) # количество товара

    def get_cost(self):
        return self.price * self.quantity

# После создания моделей необходимо выполнить миграции
# py manage.py makemigrations orders_app
# py manage.py migrate
