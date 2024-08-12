from django.urls import path
from . import views  # импорт представлений из текущего пакета

app_name = 'orders'

urlpatterns = [
    path('create/', views.order_create, name='order_create'),  # путь к созданию заказа
    # path('created/', views.order_created, name='created'),
    path('created/<int:order_id>/', views.order_created, name='created')

]
