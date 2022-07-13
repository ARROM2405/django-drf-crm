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
              'customer_first_name', 'customer_last_name', 'lead_cost']


@admin.register(PaymentsToWeb)
class PaymentsToWebAdmin(admin.ModelAdmin):
    fields = ['web_FK', 'payment_amount', 'user_added']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    fields = ['lead_FK', 'customer_first_name', 'customer_last_name', 'status', 'sent_date',
              'delivery_city', 'delivery_street', 'delivery_house_number', 'delivery_apartment_number',
              'delivery_zip_code', 'order_operator']


@admin.register(OrderedProduct)
class OrderedProductAdmin(admin.ModelAdmin):
    fields = ['order_FK', 'product_FK', 'ordered_quantity', 'ordered_product_price']


# @admin.register(Invoice)
# class InvoiceAdmin(admin.ModelAdmin):
#     fields = ['order_FK']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    fields = ['product_name', 'product_price', 'product_category', 'product_description', 'product_image',
              'quantity_available']
