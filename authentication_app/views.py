from django.shortcuts import render, redirect

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages
from .user_form import SignUpForm, ProfileForm, LoginForm, EditProfileForm
from .models import Profile
from django.shortcuts import get_object_or_404

from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from cart_app.models import Cart, CartProduct, Product, ProductSize


@receiver(user_logged_in) # декоратор для обработки сигнала
def handle_user_login(sender, user, request, **kwargs): # функция-обработчик сигнала
    session_cart = request.session.get('cart', {}) # получаем корзину из сессии
    user_cart, created = Cart.objects.get_or_create(user=user) # получаем корзину пользователя
    for product_size_id_str, product_details in session_cart.items(): # перебираем товары в корзине из сессии
        product_id, size_id = map(int, product_size_id_str.split("_")) # получаем id товара и размера
        product = Product.objects.get(pk=product_id) # получаем товар по id
        size = ProductSize.objects.get(pk=size_id) # получаем размер по id
        cart_product, created = CartProduct.objects.get_or_create(cart=user_cart, product=product, size=size) # получаем товар в корзине пользователя
        if created:
            # Если товара еще не было в корзине пользователя, просто добавляем его
            cart_product.quantity = product_details['quantity']
        else:
            # Если товар уже был в корзине пользователя, заменяем количество на большее значение
            cart_product.quantity = max(cart_product.quantity, product_details['quantity'])
        cart_product.save()

    # Очистка корзины сессии
    request.session['cart'] = {}



def profile_view(request):
    if request.user.is_authenticated:
        profile = get_object_or_404(Profile, user=request.user)
        return render(request, 'profile.html', {'profile': profile})
    else:
        return redirect('login') # если пользователь не авторизован, перенаправляем на страницу авторизации



def signup_view(request):
    '''Представление для регистрации нового пользователя'''
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        profile_form = ProfileForm(request.POST, request.FILES)
        if form.is_valid() and profile_form.is_valid():
            user = form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
        profile_form = ProfileForm()
    return render(request, 'signup.html', {'form': form, 'profile_form': profile_form})

from django.contrib.auth import get_user_model

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            # Очистите все старые сообщения
            messages.set_level(request, messages.ERROR)
            storage = messages.get_messages(request)
            storage.used = True

            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            '''Нужно получить пользователя по email и аутентифицировать его по паролю'''
            User = get_user_model() # получаем модель пользователя
            try: # пытаемся получить пользователя по email
                user = User.objects.get(email=email)
                print('найден email:', email)
            except User.DoesNotExist: # если пользователя нет, то user = None
                user = None
                print('не найден email:', email)
            if user is not None: # если пользователь существует
                user = authenticate(username=user.username, password=password)
                if user is not None: # если пользователь аутентифицирован
                    print('аутентификация прошла успешно')
                    login(request, user)
                    next_url = request.GET.get('next')  # получаем URL из параметра 'next'
                    if next_url:  # если он существует
                        return redirect(next_url)  # перенаправляем на него
                    else:
                        return redirect('home')  # иначе перенаправляем на страницу по умолчанию
                else: # если пароль не верный
                    messages.error(request, 'Неверный пароль')
            else: # если пользователя нет
                print('Пользователь с таким email не найден')
                messages.error(request, 'Пользователь с таким email не найден')
    else: # если метод GET
        form = LoginForm()
    return render(request, 'login.html', {'form': form, 'title': 'Авторизация'})


def logout_view(request):
    '''Представление для выхода пользователя'''
    logout(request)
    return redirect('home') # не забыть создать представление home и маршрут к нему

def edit_profile_view(request): # представление для редактирования профиля
    if request.user.is_authenticated: # если пользователь авторизован
        profile = get_object_or_404(Profile, user=request.user)
        print('113')
        if request.method == 'POST': # если метод POST
            print('115')
            form = EditProfileForm(request.POST, instance=profile)
            if form.is_valid():
                print('118')
                form.save()
                return redirect('profile') # перенаправляем на страницу профиля
        else:
            print('122')
            form = EditProfileForm(instance=profile)
        return render(request, 'profile_edit.html', {'form': form})
    else:
        return redirect('login')



