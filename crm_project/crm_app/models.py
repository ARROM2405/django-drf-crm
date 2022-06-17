from django.contrib.auth.models import User
from django.db import models
from django.core.validators import MinValueValidator, RegexValidator
from django.utils.timezone import now


class Profile(models.Model):
    """Keeps the role of the profile"""
    ROLES = [
        ('OP', 'Operator'),
        ('SM', 'Stock manager'),
        ('PE', 'Payments executive'),
        ('AD', 'Administrator'),
        ('TR', 'Test role')
             ]
    user = models.OneToOneField(to=User, on_delete=models.CASCADE, verbose_name='Refered user')
    role = models.CharField(max_length=30, choices=ROLES, default='TR', verbose_name='Role')


class ProductCategories(models.Model):
    """Categories of products"""
    category_name = models.CharField(max_length=50, verbose_name='Category name')

    def __str__(self):
        return f'{self.category_name}'


class Product(models.Model):
    """Information on the product"""
    product_name = models.CharField(max_length=50, verbose_name='Product name')
    product_price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)],
                                        verbose_name='Product price')
    product_category = models.ForeignKey(to=ProductCategories, on_delete=models.SET_NULL, null=True,
                                         verbose_name='Product category if exists')
    product_removed_category = models.BooleanField(default=False,
                                                   verbose_name='Product category if not exist (deleted)')
    product_description = models.TextField(verbose_name='Description of a product')
    product_image = models.FileField(upload_to='image_pics', verbose_name='Image of a product')
    quantity_available = models.IntegerField(validators=[MinValueValidator(0)],
                                             verbose_name='Available quantity of products')

    def __str__(self):
        return f'{self.product_name}'


class Web(models.Model):
    """Web is the provider of the leads"""
    web_name = models.CharField(max_length=30, verbose_name='Name of a web')
    web_description = models.TextField(blank=True, null=True, verbose_name='Description of a web')
    web_api_id = models.IntegerField(validators=[MinValueValidator(0)], verbose_name='ID for API')
    web_api_key = models.CharField(max_length=24, verbose_name='Key for API')
    balance = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Balance of a web')

    def __str__(self):
        return f'{self.web_name}'


class Offer(models.Model):
    """Keeps information of the fees for an offer"""
    web = models.ForeignKey(to=Web, on_delete=models.CASCADE, verbose_name='Web')
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE, verbose_name='Product')
    click_cost = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)],
                                     verbose_name='Cost of a click')
    website_url = models.URLField(blank=True, null=True, verbose_name='URL of a landing')

    def __str__(self):
        return f'{self.web.name}: {self.product.name}'


class Lead(models.Model):
    """Connected to offer"""
    LEAD_STATUSES = [
        ('AP', 'Approved'),
        ('RE', 'Reject'),
        ('NP', 'Not processed'),
        ('NA', 'Not answered')
    ]

    status = models.CharField(max_length=2, choices=LEAD_STATUSES, default='NP', verbose_name='Lead status')
    phone_regex_validator = RegexValidator(regex=r'\d{3}-\d{3}-\d{3}',
                                           message='Phone should be entered in a 123-456-789 format')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Lead created date and time')
    processed_at = models.DateTimeField(null=True, verbose_name='Lead processed date and time')
    offer_FK = models.ForeignKey(to=Offer, on_delete=models.SET_NULL, null=True, verbose_name='Offer FK')
    offer_removed = models.BooleanField(default=False, verbose_name='Offer of the lead if not exists(removed)')
    contact_phone = models.CharField(max_length=11, validators=[phone_regex_validator], default='123-123-123',
                                     verbose_name='Contact phone')
    customer_first_name = models.CharField(max_length=25, verbose_name='Customer first name')
    customer_last_name = models.CharField(max_length=25, blank=True, null=True, verbose_name='Customer last name')
    product_FK = models.ForeignKey(to=Product, on_delete=models.SET_NULL, null=True, verbose_name='Product FK')
    product_name = models.CharField(max_length=50, verbose_name='Product name')
    web_FK = models.ForeignKey(to=Web, on_delete=models.SET_NULL, null=True, verbose_name='Web FK')
    web_name = models.CharField(max_length=30, verbose_name='Web name')
    lead_cost = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)],
                                    verbose_name='Cost of the lead')


class PaymentsToWeb(models.Model):
    """Used to keep track of the payments made to the Webs"""
    web_FK = models.ForeignKey(to=Web, on_delete=models.SET_NULL, null=True, verbose_name='Web FK')
    web_name = models.CharField(max_length=30, verbose_name='Web name')
    payment_amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)],
                                         verbose_name='Amount paid')
    payment_date = models.DateTimeField(auto_now_add=True, verbose_name='Payment date and time')

    def __str__(self):
        return f'{self.web_name}, {self.payment_amount}'


class Order(models.Model):
    """Lead can be converted to the order"""
    ORDER_STATUSES = [
        ('NO', 'New order'),
        ('IP', 'In preparation'),
        ('SE', 'Sent'),
        ('DE', 'Delivered'),
        ('RE', 'Return'),
        ('MR', 'Money received'),
        ('CR', 'Confirmed return'),
        ('CN', 'Canceled'),
    ]
    order_created = models.DateTimeField(auto_now_add=True, verbose_name='Order created date and time')
    lead_FK = models.ForeignKey(to=Lead, on_delete=models.SET_NULL, null=True, verbose_name='Lead FK')
    customer_first_name = models.CharField(max_length=25, verbose_name='Customer first name')
    customer_last_name = models.CharField(max_length=25, blank=True, null=True, verbose_name='Customer last name')
    status = models.CharField(max_length=30, choices=ORDER_STATUSES, default='NO', verbose_name='Order Status')
    sent_date = models.DateField(auto_now_add=True, verbose_name='Send date for the order')
    order_operator = models.ForeignKey(to=User, on_delete=models.SET_NULL, null=True, verbose_name='Operator FK')
    order_operator_login = models.CharField(max_length=30, verbose_name='Operator login')


class OrderedProduct(models.Model):
    """Keeping track of the  products added to the order. Union model between Order and Product models"""
    order_FK = models.ForeignKey(to=Order, on_delete=models.SET_NULL, null=True, verbose_name='Order FK')
    product_FK = models.ForeignKey(to=Product, on_delete=models.SET_NULL, null=True, verbose_name='Product FK')
    ordered_quantity = models.IntegerField(validators=[MinValueValidator(0)], verbose_name='Ordered quantity')
    ordered_product_price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)],
                                                verbose_name='Ordered product total price')

    def __str__(self):
        return f'{self.product_FK.name}: {self.product_FK.name}'


class Invoice(models.Model):
    """Invoice generated file for the order"""
    invoice_number = models.IntegerField(verbose_name='Invoice number')
