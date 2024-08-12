from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from .models import Cart, CartProduct
from products_app.models import Product, ProductSize, ProductSizeQuantity
from django.contrib import messages
from django.http import JsonResponse  # для отправки ответа в формате JSON

def add_to_cart(request, product_id):
    '''Добавление товара в корзину'''
    product = get_object_or_404(Product, pk=product_id)
    size = get_object_or_404(ProductSize, pk=request.POST.get('size'))
    product_size_quantity = get_object_or_404(ProductSizeQuantity, product=product, size=size)  # получаем размер товара
    if request.user.is_authenticated:  # если пользователь авторизован
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_product, created = CartProduct.objects.get_or_create(
            cart=cart, product=product, size=size
        )
        if not created:  # если товар уже есть в корзине
            if cart_product.quantity < product_size_quantity.quantity:
                cart_product.quantity += 1
                cart_product.save()
            else:  # если количество товара в корзине равно количеству на складе
                messages.error(request,
                               f'Вы добавили максимальное количество, доступно {product_size_quantity.quantity} шт.')
        return redirect(request.META.get('HTTP_REFERER'))  # Добавлено возвращение ответа
    else:  # если пользователь не авторизован
        cart = request.session.get('cart', {})
        product_size_id = str(product_id) + '_' + str(size.id)  # создаем уникальный идентификатор товара
        # если товар с таким размером уже есть в корзине
        if product_size_id in cart:  # если товар есть в корзине
            if cart[product_size_id][
                'quantity'] < product_size_quantity.quantity:  # если количество товара в корзине меньше, чем на складе
                cart[product_size_id]['quantity'] += 1
            else:  # если количество товара в корзине равно количеству на складе
                messages.error(request,
                               f'Вы добавили максимальное количество, доступно {product_size_quantity.quantity} шт.')
        else:  # если товара с таким размером нет в корзине
            cart[product_size_id] = {'quantity': 1, 'size': size.id}  # добавляем товар в корзину
        request.session['cart'] = cart  # сохраняем корзину в сессии
        messages.success(request, f'В корзине {product.name} {size.size} {cart[product_size_id]["quantity"]} шт.')
        return redirect(request.META.get('HTTP_REFERER'))


def remove_from_cart(request, product_id, size_id):
    '''Удаление товара из корзины'''
    print('Удаление товара из корзины 48')
    product = get_object_or_404(Product, pk=product_id)
    size = get_object_or_404(ProductSize, pk=size_id)
    if request.user.is_authenticated: # если пользователь авторизован
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_product = get_object_or_404(CartProduct, cart=cart, product=product, size=size)
        print('Удаление товара из корзины 54')
        cart_product.delete()
        print('Удаление товара из корзины 56')
    else:
        cart = request.session.get('cart', {})
        product_size_id = str(product_id) + '_' + str(size_id)
        if product_size_id in cart:
            del cart[product_size_id]
            request.session['cart'] = cart
            request.session.modified = True
    return redirect('cart_view')


def change_quantity(request, product_id):
    '''Изменение количества товара в корзине'''
    product = get_object_or_404(Product, pk=product_id)
    size = get_object_or_404(ProductSize, pk=request.POST.get('size'))
    product_size_quantity = get_object_or_404(ProductSizeQuantity, product=product, size=size)
    new_quantity = request.POST.get('quantity')
    if new_quantity:  # если новое количество товара передано
        new_quantity = int(new_quantity)
        if request.user.is_authenticated:  # если пользователь авторизован
            cart, created = Cart.objects.get_or_create(user=request.user)
            cart_product = get_object_or_404(CartProduct, cart=cart, product=product, size=size)
            if product_size_quantity.quantity >= new_quantity:  # если количество товара на складе больше или равно новому количеству
                cart_product.quantity = new_quantity  # устанавливаем новое количество товара
                cart_product.save()
                cart_product.refresh_from_db()  # обновляем данные из базы
            else:
                messages.error(request, f'Недостаточное количество !!!')
                messages.error(request,
                               f'{product.name} {size.size}, максимально доступное кол {product_size_quantity.quantity} шт.')
        else:  # если пользователь не авторизован
            cart = request.session.get('cart', {})
            product_size_id = str(product_id) + '_' + str(size.id)
            if product_size_id in cart:
                if product_size_quantity.quantity >= new_quantity:
                    cart[product_size_id]['quantity'] = new_quantity
                    request.session['cart'] = cart
                    request.session.modified = True
                else:
                    messages.error(request, f'Недостаточное количество !!!')
                    messages.error(request,
                                   f'{product.name} {size.size}, максимально доступное кол {product_size_quantity.quantity} шт.')
    return redirect('cart_view')


def cart_view(request):
    # '''Представление для корзины покупок'''
    # if 'cart' in request.session:
    #     del request.session['cart']

    if request.user.is_authenticated:  # если пользователь авторизован
        cart, created = Cart.objects.get_or_create(user=request.user)  # получаем корзину пользователя
        cart_products = CartProduct.objects.filter(cart=cart)  # получаем товары в корзине
    else:  # если пользователь не авторизован
        cart = request.session.get('cart',
                                   {})  # получаем корзину из сессии или пустой словарь если корзины нет в сессии
        cart_products = []  # создаем пустой список для товаров в корзине
        for product_size_id_str, product_details in cart.items():  # перебираем товары в корзине
            product_id, size_id = map(int, product_size_id_str.split("_"))
            product = Product.objects.get(pk=product_id)  # получаем товар по id из корзины
            cart_products.append({'product': product,
                                  'quantity': product_details['quantity'],
                                  'size': ProductSize.objects.get(
                                      pk=product_details['size'])})  # добавляем товар в список товаров в корзине
    total_quantity = 0
    total_price = 0
    for cart_product in cart_products:
        if request.user.is_authenticated:
            total_quantity += cart_product.quantity
            total_price += cart_product.product.price * cart_product.quantity
        else:
            total_quantity += cart_product['quantity']
            total_price += cart_product['product'].price * cart_product['quantity']

    return render(request, 'cart.html',
                  {'cart_products': cart_products, 'total_quantity': total_quantity, 'total_price': total_price})

    # return render(request, 'cart.html', {'cart_products': cart_products})  # передача данных в шаблон
def check_availability(request, product_id, size_id):
    if request.user.is_authenticated:  # если пользователь авторизован
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_products = CartProduct.objects.filter(cart=cart)
    else:  # если пользователь не авторизован
        cart = request.session.get('cart', {})
        cart_products = []
        for product_size_id_str, product_details in cart.items():  # перебираем товары в корзине
            product_id, size_id = map(int, product_size_id_str.split("_"))
            product = Product.objects.get(pk=product_id)
            cart_products.append({'product': product,
                                  'quantity': product_details['quantity'],
                                  'size': ProductSize.objects.get(
                                      pk=product_details['size'])})  # добавляем товар в список товаров в корзине

    availability = {}  # словарь для хранения наличия товара
    for cart_product in cart_products:  # перебираем товары в корзине
        if request.user.is_authenticated:
            product_size_quantity = get_object_or_404(ProductSizeQuantity, product=cart_product.product,
                                                      size=cart_product.size)
            availability[
                str(cart_product.product.id) + "_" + str(cart_product.size.id)] = product_size_quantity.quantity
        else:
            product_size_quantity = get_object_or_404(ProductSizeQuantity, product=cart_product['product'],
                                                      size=cart_product['size'])
            availability[
                str(cart_product['product'].id) + "_" + str(cart_product['size'].id)] = product_size_quantity.quantity
    print(availability)
    return JsonResponse(availability)  # возвращаем ответ в формате JSON


def order_view(request):
    '''Представление для оформления заказа'''
    # добавить логику для оформления заказа
    pass
