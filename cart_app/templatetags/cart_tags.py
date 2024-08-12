from django import template

'''Шаблонный тег для подсчета общей стоимости товара'''

register = template.Library()

@register.filter
def total_price(price, quantity):
    return price * quantity
