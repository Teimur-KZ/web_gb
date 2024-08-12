from django.urls import path
from . import views # импорт представлений из текущего пакета
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup_view, name='signup'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.edit_profile_view, name='edit_profile'),
] #+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
