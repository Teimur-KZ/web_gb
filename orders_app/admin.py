from django.contrib import admin

# Register your models here.
from .models import Order, DeliveryOptions, PaymentOptions, OrderItemNew
class OrderItemInline(admin.TabularInline):
    model = OrderItemNew
    raw_id_fields = ['product_size_quantity'] # поле для поиска товара по id
    fields = ('product_size_quantity', 'quantity', 'price') # добавляем поля для отображения
    readonly_fields = ('product_size_quantity', 'quantity', 'price') # делаем эти поля только для чтения

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['number_order', 'user_profile', 'created', 'updated', 'payment', 'paid', 'delivery', 'delivery_price', 'delivery_status', 'total_price']
    list_filter = ['paid', 'created', 'updated']
    inlines = [OrderItemInline]
    extra = 0

class DeliveryOptionsAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'min_total_price_for_free_delivery')
    list_editable = ('price', 'min_total_price_for_free_delivery')

class PaymentOptionsAdmin(admin.ModelAdmin):
    list_display = ('name',)

admin.site.register(DeliveryOptions, DeliveryOptionsAdmin)
admin.site.register(PaymentOptions, PaymentOptionsAdmin)



