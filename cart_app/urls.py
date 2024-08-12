from django.urls import path
from . import views # импорт представлений из текущего пакета
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.cart_view, name='cart'), # путь к представлению корзины
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'), # путь к представлению добавления в корзину
    path('cart_view/', views.cart_view, name='cart_view'), # путь к представлению корзины
    #path('remove_from_cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'), # путь к представлению удаления из корзины
    path('remove_from_cart/<int:product_id>/<int:size_id>/', views.remove_from_cart, name='remove_from_cart'), # путь к представлению удаления из корзины
    #path('change_quantity/<int:product_id>/<int:quantity>/', views.change_quantity, name='change_quantity'), # путь к представлению изменения количества товара
    path('change_quantity/<int:product_id>/', views.change_quantity, name='change_quantity'),
    path('check_availability/<int:product_id>/<int:size_id>/', views.check_availability, name='check_availability'),
    path('cart/change_quantity/<int:product_id>/', views.change_quantity, name='change_quantity'),



] #+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)