from django.shortcuts import render, get_object_or_404
from .models import Product, Category, ProductSizeQuantity
from django.db.models import Sum

def category_all(request):
    '''Отображение всех категорий'''
    categories = Category.objects.all()  # получение всех категорий
    return render(request, 'category_all.html', {'categories': categories})  # передача данных в шаблон

def product_category(request, category):
    '''Отображение товаров по категориям'''
    category_obj = get_object_or_404(Category, name=category)  # получение объекта категории или 404
    products = Product.objects.filter(category=category_obj)  # получение товаров по категории
    for product in products:
        product.quantity = ProductSizeQuantity.objects.filter(product=product).aggregate(Sum('quantity'))['quantity__sum'] or 0
    return render(request, 'product_category.html', {'products': products, 'category': category_obj})  # передача данных в шаблон

def product_info(request, product_id):
    '''Отображение информации о товаре'''
    product = get_object_or_404(Product, pk=product_id)  # получение товара по id или 404
    productSizeQuantity = ProductSizeQuantity.objects.filter(product=product, quantity__gt=0)  # получение размеров и количества товара
    category = product.category.name
    request.session['next'] = request.get_full_path()  # сохранение текущего url в сессии отличается от request.path тем, что включает GET-параметры
    return render(request, 'product_info.html', {
        'product': product,
        'productSizeQuantity': productSizeQuantity,
        'category': category,
        'seo_title': product.seo_title or product.name,
        'seo_description': product.seo_description or product.description,
        'seo_keywords': product.seo_keywords or product.name
    })  # передача данных в шаблон

