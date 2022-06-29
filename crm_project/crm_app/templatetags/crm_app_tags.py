from django import template
from ..models import OrderedProduct

register = template.Library()


@register.filter(name='order_total_price')
def order_total_price(order):
    total_price = 0.0
    for ordered_product in OrderedProduct.objects.filter(order_FK=order):
        total_price += ordered_product.total_price()
    return total_price
