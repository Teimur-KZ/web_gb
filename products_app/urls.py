from django.urls import path
from . import views # импорт представлений из текущего пакета
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('category_all/', views.category_all, name='category_all'), # путь к представлению category_all
    path('product_category/<str:category>/', views.product_category, name='product_category'), # путь к представлению product_category
    path('product_info/<int:product_id>/', views.product_info, name='product_info'), # путь к представлению product_info
] #+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)