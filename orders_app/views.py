from django.shortcuts import render

# Create your views here.
from django.shortcuts import redirect
from .models import Order, OrderItemNew, DeliveryOptions
from .order_form import OrderCreateForm
from cart_app.models import Cart, CartProduct, ProductSizeQuantity
import uuid  # для генерации уникального номера заказа
from django.shortcuts import get_object_or_404
from django.urls import reverse



def order_create(request):
    if request.user.is_authenticated:  # проверка авторизации пользователя
        cart = Cart.objects.get(user=request.user)
        total_price = cart.get_total_price()
        delivery = DeliveryOptions.objects.filter(min_total_price_for_free_delivery__lte=total_price).order_by('-min_total_price_for_free_delivery').first()
        delivery_price =delivery.price
        print('сумма заказа', total_price, 'доставка', delivery, 'стоимость доставки', delivery.price)

        if request.method == 'POST': # если форма отправлена
            form = OrderCreateForm(request.POST, initial={'cart': cart, 'delivery': delivery})
            if form.is_valid(): # если форма валидна
                order = form.save(commit=False)
                order.user_profile = request.user.profile
                order.total_price = total_price
                order.delivery_price = delivery_price
                order.save()
                #order.number_order = str(uuid.uuid4())  # генерируем уникальный номер заказа
                order.number_order = str(order.id)
                print('номер заказа', order.number_order)
                order.save()
                for item in cart.cartproduct_set.all(): # перебираем товары в корзине
                    product_size_quantity = get_object_or_404(ProductSizeQuantity, product=item.product, size=item.size)
                    OrderItemNew.objects.create(
                        order=order,
                        product_size_quantity=product_size_quantity,
                        price=item.product.price,
                        quantity=item.quantity,
                    )
                    product_size_quantity.quantity -= item.quantity
                    product_size_quantity.save()
                #cart.clean()
                cart.products.clear()
                #return redirect('orders_app:created', order_id=order.id) #order_id=order.id
                return redirect('orders:created', order_id=order.id) # order: - это namespace из urls.py

        else: # если форма не отправлена
            form = OrderCreateForm(initial={'cart': cart, 'delivery': delivery})
        total_quantity = cart.get_total_quantity()  # получаем общее количество товаров
        return render(request, 'create.html',
                      {'form': form, 'total_quantity': total_quantity, 'total_price': total_price,
                       'delivery_price': delivery_price})
    else: # если пользователь не авторизован
        login_url = reverse('login')
        next_url = request.get_full_path()  # получаем текущий URL
        return redirect(f'{login_url}?next={next_url}')  # добавляем его в параметр 'next'


#def order_created(request):  # страница успешного создания заказа
def order_created(request, order_id):  # добавляем order_id в качестве аргумента
    order = Order.objects.get(id=order_id)  # получаем объект Order
    return render(request, 'created.html', {'order': order})  # передаем объект Order в контекст
