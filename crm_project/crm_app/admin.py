from django.contrib import admin
from .models import *


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    fields = ['user', 'role']


@admin.register(ProductCategory)
class ProductCategories(admin.ModelAdmin):
    fields = ['category_name']


@admin.register(Web)
class WebAdmin(admin.ModelAdmin):
    fields = ['web_name', 'web_description', 'web_api_key', 'balance']


@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    fields = ['web', 'product', 'click_cost', 'website_url']


@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    fields = ['status', 'processed_at', 'offer_FK', 'offer_removed', 'contact_phone',
              'customer_first_name', 'customer_last_name', 'product_FK', 'product_name', 'web_FK',
              'web_name', 'lead_cost']


@admin.register(PaymentsToWeb)
class PaymentsToWebAdmin(admin.ModelAdmin):
    fields = ['web_FK', 'web_name', 'payment_amount']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    fields = ['lead_FK', 'customer_first_name', 'customer_last_name', 'status', 'sent_date',
              'order_operator', 'order_operator_login']


@admin.register(OrderedProduct)
class OrderedProductAdmin(admin.ModelAdmin):
    fields = ['order_FK', 'product_FK', 'ordered_quantity', 'ordered_product_price']


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    fields = ['order_FK']
