from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='<font color=red>*</font>')
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput,
                                help_text='<font color=red>*</font><br>'+
                                          '<font size=2>- Пароль должен содержать не менее 8 символов</font><br>' +
                                          '<font size=2>- не быть слишком распространенным и не совпадать с другими вашими данными.</font><br>' +
                                          '<font size=2>- Пароль не может состоять только из цифр.</font><br>')
    password2 = forms.CharField(label='Подтверждение пароля', widget=forms.PasswordInput, help_text='<font color=red>*</font>')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', )
        labels = {'username': 'Имя пользователя', 'email': 'Электронная почта', 'password1': 'Пароль',
                  'password2': 'Подтверждение пароля'}

class ProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=100, label='Имя')  # поле для ввода имени
    last_name = forms.CharField(max_length=100, label='Фамилия', required=False)  # поле для ввода фамилии
    phone_number = forms.CharField(max_length=20, label='Телефон', required=False)  # поле для ввода телефона
    avatar = forms.ImageField(label='Аватар', required=False)  # поле для загрузки аватара
    date_of_birth = forms.DateField(label='Дата рождения', required=False,
                            widget=forms.DateInput(attrs={'class': 'form-control',
                                                            'type': 'date'}))
    adress_of_delivery_line_1 = forms.CharField(max_length=100, label='Адрес доставки 1',
                                                required=True)  # поле для ввода адреса доставки
    adress_of_delivery_line_2 = forms.CharField(max_length=100, label='Адрес доставки 2',
                                                required=False)  # поле для ввода адреса доставки
    adress_of_city = forms.CharField(max_length=100, label='Город', required=True)  # поле для ввода города
    adress_of_state = forms.CharField(max_length=100, label='Область', required=False)  # поле для ввода области
    adress_of_zip = forms.CharField(max_length=10, label='Индекс', required=True)  # поле для ввода индекса

    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'phone_number', 'avatar', 'date_of_birth',
                  'adress_of_delivery_line_1', 'adress_of_delivery_line_2', 'adress_of_city', 'adress_of_state',
                  'adress_of_zip']
        labels = {'first_name': 'Имя', 'last_name': 'Фамилия', 'phone_number': 'Телефон', 'avatar': 'Аватар',
                    'date_of_birth': 'Дата рождения', 'adress_of_delivery_line_1': 'Адрес доставки (улица, дом)',
                    'adress_of_delivery_line_2': 'Адрес доставки (квартира)', 'adress_of_city': 'Город', 'adress_of_state': 'Область',
                    'adress_of_zip': 'Индекс'}


class EditProfileForm(forms.ModelForm): # форма для редактирования профиля
    first_name = forms.CharField(max_length=100, label='Имя')  # поле для ввода имени
    last_name = forms.CharField(max_length=100, label='Фамилия', required=False)  # поле для ввода фамилии
    phone_number = forms.CharField(max_length=20, label='Телефон', required=False)  # поле для ввода телефона
    avatar = forms.ImageField(label='Аватар', required=False)  # поле для загрузки аватара
    date_of_birth = forms.DateField(label='Дата рождения', required=False,
                            widget=forms.DateInput(attrs={'class': 'form-control',
                                                            'type': 'date'}))
    adress_of_delivery_line_1 = forms.CharField(max_length=100, label='Адрес доставки 1',
                                                required=True)  # поле для ввода адреса доставки
    adress_of_delivery_line_2 = forms.CharField(max_length=100, label='Адрес доставки 2',
                                                required=False)  # поле для ввода адреса доставки
    adress_of_city = forms.CharField(max_length=100, label='Город', required=True)  # поле для ввода города
    adress_of_state = forms.CharField(max_length=100, label='Область', required=False)  # поле для ввода области
    adress_of_zip = forms.CharField(max_length=10, label='Индекс', required=True)  # поле для ввода индекса
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'date_of_birth', 'phone_number', 'avatar',
                  'adress_of_delivery_line_1', 'adress_of_delivery_line_2', 'adress_of_city', 'adress_of_state',
                  'adress_of_zip']
        labels = {'first_name': 'Имя', 'last_name': 'Фамилия', 'date_of_birth': 'Дата рождения', 'phone_number': 'Телефон', 'avatar': 'Аватар',
                    'adress_of_delivery_line_1': 'Адрес доставки (улица, дом)',
                    'adress_of_delivery_line_2': 'Адрес доставки (квартира)', 'adress_of_city': 'Город', 'adress_of_state': 'Область',
                    'adress_of_zip': 'Индекс'}



class LoginForm(forms.Form):
    email = forms.EmailField(label='Электронная почта', max_length=100)
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)
