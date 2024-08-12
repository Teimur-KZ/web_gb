from django.urls import path
from . import views # импорт представлений из текущего пакета

urlpatterns = [
    path('', views.home_view, name='home'),
    path('contacts/', views.contacts_view, name='contacts'),
    path('about/', views.about_view, name='about'),
    ]
