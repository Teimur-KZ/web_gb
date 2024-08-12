from django import forms
from .models import Order
from cart_app.models import ProductSizeQuantity
from django.shortcuts import get_object_or_404

class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['payment', 'comment', 'delivery']
        labels = {'payment': 'Способ оплаты', 'comment': 'Комментарий', 'delivery': 'Способ доставки'}
        widgets = {
            'payment': forms.Select(attrs={'class': 'form-control'}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'delivery': forms.HiddenInput(),  # используем HiddenInput для скрытия поля
        }

    def clean(self):
        cleaned_data = super().clean()
        cart = self.initial.get('cart')
        for item in cart.cartproduct_set.all():
            product_size_quantity = get_object_or_404(ProductSizeQuantity, product=item.product, size=item.size)
            if item.quantity > product_size_quantity.quantity:
                raise forms.ValidationError(f"Товар {item.product.name} недоступен в требуемом количестве.")
        return cleaned_data

