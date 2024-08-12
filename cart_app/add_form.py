'''Форма добавления товара в корзину'''

from django import forms
from products_app.models import Product,ProductSizeQuantity
from django.core.exceptions import ValidationError # импорт исключения ValidationError
from django.shortcuts import get_object_or_404

class AddToCartForm(forms.Form):
    quantity = forms.IntegerField(label='Количество товара', min_value=1, required=True) # min_value - минимальное значение
    size = forms.ModelChoiceField(queryset=ProductSizeQuantity.objects.all(), required=True)

    def clean(self):
        cleaned_data = super().clean()
        quantity = cleaned_data.get('quantity')
        product_id = self.initial.get('product_id')
        size = cleaned_data.get('size')

        if product_id and size:
            product_size_quantity = get_object_or_404(ProductSizeQuantity, product_id=product_id, size=size)
            if quantity > product_size_quantity.quantity:
                raise ValidationError('Количество товара превышает доступное количество')
        return cleaned_data


