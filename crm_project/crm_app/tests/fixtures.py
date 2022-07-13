import datetime

import pytest
from ..models import *


@pytest.fixture
def create_user(db, django_user_model):
    def make_user(
            username='test_username',
            password='test_password'
    ):
        return django_user_model.objects.create(
            username=username,
            password=password
        )

    return make_user


@pytest.fixture
def create_profile(db, create_user):
    def make_profile(
            username='test_username',
            password='test_password',
            role='Operator'
    ):
        user = create_user(username=username, password=password)
        return Profile.objects.create(
            user=user,
            role=role
        )

    return make_profile


@pytest.fixture
def create_product_category(db):
    def make_product_category(category_name='test_category_name'):
        return ProductCategory.objects.create(
            category_name=category_name
        )

    return make_product_category


@pytest.fixture
def create_product(db):
    def make_product(
            product_category: ProductCategory,
            product_name='test_product_name',
            product_price=5.0,
            product_description='test_description',
            quantity_available=50,
            quantity_in_delivery=10
    ):
        return Product.objects.create(
            product_name=product_name,
            product_price=product_price,
            product_category=product_category,
            product_description=product_description,
            quantity_available=quantity_available,
            quantity_in_delivery=quantity_in_delivery
        )

    return make_product


@pytest.fixture
def create_web(db):
    def make_web(
            web_name='test_web',
            web_description='test_description',
            web_api_key='1234567890',
            balance=100
    ):
        return Web.objects.create(
            web_name=web_name,
            web_description=web_description,
            web_api_key=web_api_key,
            balance=balance
        )

    return make_web


@pytest.fixture
def create_offer(db):
    def make_offer(
            product: Product,
            web: Web,
            click_cost=35.0
    ):
        return Offer.objects.create(
            web=web,
            product=product,
            click_cost=click_cost
        )

    return make_offer


@pytest.fixture
def create_lead(db):
    def make_lead(
            offer: Offer,
            operator_assigned: Profile = None,
            status='Not processed',
            contact_phone='123-123-123',
            customer_first_name='test_customer_fn',
            customer_last_name='test_customer_ln',
            lead_cost=35.0
    ):
        return Lead.objects.create(
            status=status,
            offer_FK=offer,
            contact_phone=contact_phone,
            customer_first_name=customer_first_name,
            customer_last_name=customer_last_name,
            lead_cost=lead_cost,
            operator_assigned=operator_assigned
        )

    return make_lead


@pytest.fixture
def create_payment_to_web(db):
    def make_payment_to_web(
            web: Web,
            user_added: User,
            payment_amount=50.5,
    ):
        return PaymentsToWeb.objects.create(
            web_FK=web,
            payment_amount=payment_amount,
            user_added=user_added
        )

    return make_payment_to_web


@pytest.fixture
def create_order(db):
    def make_order(
            lead: Lead = None,
            order_operator: User = None,
            customer_first_name='test_customer_fn',
            customer_last_name='test_customer_ln',
            status='New order',
            sent_date=datetime.date.today(),
            contact_phone='123-123-123',
            delivery_city='test_city',
            delivery_street='test_street',
            delivery_zip_code='12345',
    ):
        return Order.objects.create(
            lead_FK=lead,
            customer_first_name=customer_first_name,
            customer_last_name=customer_last_name,
            status=status,
            sent_date=sent_date,
            contact_phone=contact_phone,
            delivery_city=delivery_city,
            delivery_street=delivery_street,
            delivery_zip_code=delivery_zip_code,
            order_operator=order_operator
        )

    return make_order


@pytest.fixture
def create_ordered_product(db):
    def make_ordered_product(
            order: Order = None,
            product: Product = None,
            ordered_quantity=3,
            ordered_product_price=50.0
    ):
        return OrderedProduct.objects.create(
            order_FK=order,
            product_FK=product,
            ordered_quantity=ordered_quantity,
            ordered_product_price=ordered_product_price
        )

    return make_ordered_product
