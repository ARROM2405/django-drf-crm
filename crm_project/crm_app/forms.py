from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from django import forms

from .models import *


class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['username'].label = 'type in username'
        self.fields['username'].help_text = None
        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = None


class WebCreationForm(ModelForm):
    class Meta:
        model = Web
        fields = ['web_name', 'web_description', 'web_api_key', 'balance']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['web_description'].widget.attrs['rows'] = 2


class LeadCreationForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['contact_phone'].widget.attrs['placeholder'] = '123-123-123'

    class Meta:
        model = Lead
        fields = ['offer_FK', 'contact_phone', 'customer_first_name', 'customer_last_name']


class ProductCategoryCreationForm(ModelForm):
    class Meta:
        model = ProductCategory
        fields = ['category_name']


class ProductCreationForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['product_category'].label = 'Product category'
        self.fields['product_description'].widget.attrs['rows'] = 4

    class Meta:
        model = Product
        fields = ['product_name', 'product_price', 'product_category', 'product_description', 'product_image',
                  'quantity_available']


class OfferCreationForm(ModelForm):
    class Meta:
        model = Offer
        fields = ['web', 'product', 'click_cost', 'website_url']


class PaymentCreationForm(ModelForm):
    class Meta:
        model = PaymentsToWeb
        fields = ['web_FK', 'payment_amount']


class OrderCreationForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['product_1'] = forms.ModelChoiceField(queryset=Product.objects.filter(quantity_available__gt=0))
        self.fields['product_1_quantity'] = forms.IntegerField()
        self.fields['product_1_quantity'].widget.attrs['min'] = 1
        self.fields['product_1_price'] = forms.FloatField()
        self.fields['product_1_price'].widget.attrs['min'] = 0

        self.fields['product_2'] = forms.ModelChoiceField(queryset=Product.objects.filter(quantity_available__gt=0),
                                                          required=False)
        self.fields['product_2_quantity'] = forms.IntegerField(required=False)
        self.fields['product_2_quantity'].widget.attrs['min'] = 1
        self.fields['product_2_price'] = forms.FloatField(required=False)
        self.fields['product_2_price'].widget.attrs['min'] = 0

        self.fields['product_3'] = forms.ModelChoiceField(queryset=Product.objects.filter(quantity_available__gt=0),
                                                          required=False)
        self.fields['product_3_quantity'] = forms.IntegerField(required=False)
        self.fields['product_3_quantity'].widget.attrs['min'] = 1
        self.fields['product_3_price'] = forms.FloatField(required=False)
        self.fields['product_3_price'].widget.attrs['min'] = 0

    class Meta:
        model = Order
        fields = ['customer_first_name', 'customer_last_name', 'status', 'sent_date', 'contact_phone', 'delivery_city',
                  'delivery_street', 'delivery_house_number', 'delivery_apartment_number', 'delivery_zip_code']