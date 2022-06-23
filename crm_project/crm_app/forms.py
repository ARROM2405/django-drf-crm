from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm

from .models import *


class RegistrationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'type in username'


class WebCreationForm(ModelForm):
    class Meta:
        model = Web
        fields = ['web_name', 'web_description', 'web_api_key', 'balance']


class LeadCreationForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['contact_phone'].help_text = 'format 123-123-123'

    class Meta:
        model = Lead
        fields = ['offer_FK', 'contact_phone', 'customer_first_name', 'customer_last_name', 'product_FK',
                  'web_FK']


class ProductCategoryCreationForm(ModelForm):
    class Meta:
        model = ProductCategory
        fields = ['category_name']


class ProductCreationForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['product_category'].label = 'Product category'


    class Meta:
        model = Product
        fields = ['product_name', 'product_price', 'product_category', 'product_description', 'product_image',
                  'quantity_available']
