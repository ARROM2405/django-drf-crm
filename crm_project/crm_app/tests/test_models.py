from crm_app.tests.fixtures import *


# Tests for Profile model
@pytest.mark.django_db
def test_profile_field_verbose_name(create_profile):
    test_profile = create_profile()
    assert test_profile._meta.get_field('user').verbose_name == 'Referred user'
    assert test_profile._meta.get_field('role').verbose_name == 'Role'
    assert test_profile._meta.get_field('blocked').verbose_name == 'Blocked user'


@pytest.mark.django_db
def test_profile_field_length(create_profile):
    test_profile = create_profile()
    assert test_profile._meta.get_field('role').max_length == 30


@pytest.mark.django_db
def test_profile_str_method(create_profile):
    test_profile = create_profile()
    assert str(test_profile) == test_profile.user.username


# Test for ProductCategory model
@pytest.mark.django_db
def test_product_category_field_verbose_name(create_product_category):
    test_category = create_product_category()
    assert test_category._meta.get_field('category_name').verbose_name == 'Category name'


@pytest.mark.django_db
def test_product_category_field_length(create_product_category):
    test_category = create_product_category()
    assert test_category._meta.get_field('category_name').max_length == 50


@pytest.mark.django_db
def test_product_category_str_method(create_product_category):
    test_category = create_product_category()
    assert str(test_category) == test_category.category_name


@pytest.mark.django_db
def test_product_category_products_in_category_count_method(create_product_category, create_product):
    test_category = create_product_category()
    products_count = 10
    for product_num in range(products_count):
        create_product(product_category=test_category,
                       product_name=f'test_product_{product_num}')
    assert test_category.products_in_category_count() == products_count


# Test for Product model
@pytest.mark.django_db
def test_product_field_verbose_name(create_product_category, create_product):
    test_category = create_product_category()
    test_product = create_product(product_category=test_category)
    assert test_product._meta.get_field('product_name').verbose_name == 'Product name'
    assert test_product._meta.get_field('product_price').verbose_name == 'Product price'
    assert test_product._meta.get_field('product_category').verbose_name == 'Product category if exists'
    assert test_product._meta.get_field('product_description').verbose_name == 'Description of a product'
    assert test_product._meta.get_field('product_image').verbose_name == 'Image of a product'
    assert test_product._meta.get_field('quantity_available').verbose_name == 'Available quantity of products'
    assert test_product._meta.get_field('quantity_in_delivery').verbose_name == 'Products in delivery to clients'


@pytest.mark.django_db
def test_product_field_min_value_validators(create_product_category, create_product):
    test_category = create_product_category()
    test_product = create_product(product_category=test_category)
    assert test_product._meta.get_field('quantity_available').validators[0] == MinValueValidator(0)
    assert test_product._meta.get_field('quantity_in_delivery').validators[0] == MinValueValidator(0)


@pytest.mark.django_db
def test_product_str_method(create_product_category, create_product):
    test_category = create_product_category()
    test_product = create_product(product_category=test_category)
    assert str(test_product) == test_product.product_name


# Tests for Web model
@pytest.mark.django_db
def test_web_field_verbose_name(create_web):
    test_web = create_web()
    assert test_web._meta.get_field('web_name').verbose_name == 'Name of a web'
    assert test_web._meta.get_field('web_description').verbose_name == 'Description of a web'
    assert test_web._meta.get_field('web_api_key').verbose_name == 'Key for API'
    assert test_web._meta.get_field('balance').verbose_name == 'Balance of a web'
    assert test_web._meta.get_field('active').verbose_name == 'Web activity status'


@pytest.mark.django_db
def test_web_field_max_length_and_max_digits_and_decimal_places(create_web):
    test_web = create_web()
    assert test_web._meta.get_field('web_name').max_length == 30
    assert test_web._meta.get_field('web_api_key').max_length == 24
    assert test_web._meta.get_field('balance').max_digits == 10
    assert test_web._meta.get_field('balance').decimal_places == 2


@pytest.mark.django_db
def test_web_str_method(create_web):
    test_web = create_web()
    assert str(test_web) == test_web.web_name


# Tests for Offer model
@pytest.mark.django_db
def test_offer_field_verbose_name(create_web, create_product_category, create_product, create_offer):
    test_web = create_web()
    test_product = create_product(product_category=create_product_category())
    test_offer = create_offer(web=test_web, product=test_product)
    assert test_offer._meta.get_field('web').verbose_name == 'Web'
    assert test_offer._meta.get_field('product').verbose_name == 'Product'
    assert test_offer._meta.get_field('click_cost').verbose_name == 'Cost of a click'
    assert test_offer._meta.get_field('website_url').verbose_name == 'URL of a landing'


def test_offer_field_max_digits_and_decimal_places(create_web, create_product_category, create_product, create_offer):
    test_web = create_web()
    test_product = create_product(product_category=create_product_category())
    test_offer = create_offer(web=test_web, product=test_product)
    assert test_offer._meta.get_field('click_cost').max_digits == 10
    assert test_offer._meta.get_field('click_cost').decimal_places == 2


@pytest.mark.django_db
def test_offer_str_method(create_web, create_product_category, create_product, create_offer):
    test_web = create_web()
    test_product = create_product(product_category=create_product_category())
    test_offer = create_offer(web=test_web, product=test_product)
    assert str(test_offer) == f'{test_offer.web.web_name}: {test_offer.product.product_name}'


# Test for Lead model
@pytest.mark.django_db
def test_lead_field_verbose_name(create_web, create_product_category, create_product, create_offer, create_lead):
    test_web = create_web()
    test_product = create_product(product_category=create_product_category())
    test_offer = create_offer(web=test_web, product=test_product)
    test_lead = create_lead(offer=test_offer)
    assert test_lead._meta.get_field('status').verbose_name == 'Lead status'
    assert test_lead._meta.get_field('created_at').verbose_name == 'Lead created date and time'
    assert test_lead._meta.get_field('processed_at').verbose_name == 'Lead processed date and time'
    assert test_lead._meta.get_field('offer_FK').verbose_name == 'Offer FK'
    assert test_lead._meta.get_field('offer_removed').verbose_name == 'Offer of the lead if not exists(removed)'
    assert test_lead._meta.get_field('contact_phone').verbose_name == 'Contact phone'
    assert test_lead._meta.get_field('customer_first_name').verbose_name == 'Customer first name'
    assert test_lead._meta.get_field('customer_last_name').verbose_name == 'Customer last name'
    assert test_lead._meta.get_field('lead_cost').verbose_name == 'Cost of the lead'
    assert test_lead._meta.get_field('operator_assigned').verbose_name == 'Operator assigned'


@pytest.mark.django_db
def test_lead_field_max_length_and_max_digits_and_decimal_places(create_web, create_product_category, create_product,
                                                                 create_offer, create_lead):
    test_web = create_web()
    test_product = create_product(product_category=create_product_category())
    test_offer = create_offer(web=test_web, product=test_product)
    test_lead = create_lead(offer=test_offer)
    assert test_lead._meta.get_field('status').max_length == 25
    assert test_lead._meta.get_field('contact_phone').max_length == 11
    assert test_lead._meta.get_field('customer_first_name').max_length == 25
    assert test_lead._meta.get_field('customer_last_name').max_length == 25
    assert test_lead._meta.get_field('lead_cost').max_digits == 10
    assert test_lead._meta.get_field('lead_cost').decimal_places == 2


@pytest.mark.django_db
def test_lead_field_min_value_validators(create_web, create_product_category, create_product,
                                         create_offer, create_lead):
    test_web = create_web()
    test_product = create_product(product_category=create_product_category())
    test_offer = create_offer(web=test_web, product=test_product)
    test_lead = create_lead(offer=test_offer)
    assert test_lead._meta.get_field('lead_cost').validators[0] == MinValueValidator(0)


@pytest.mark.django_db
def test_lead_str_method(create_web, create_product_category, create_product,
                         create_offer, create_lead):
    test_web = create_web()
    test_product = create_product(product_category=create_product_category())
    test_offer = create_offer(web=test_web, product=test_product)
    test_lead = create_lead(offer=test_offer)
    assert str(test_lead) == f'Lead {test_lead.pk}'


@pytest.mark.django_db
def test_lead_ordering(create_web, create_product_category, create_product,
                       create_offer, create_lead):
    test_web = create_web()
    test_product = create_product(product_category=create_product_category())
    test_offer = create_offer(web=test_web, product=test_product)
    for _ in range(3):
        create_lead(offer=test_offer)
    test_leads = Lead.objects.all()
    assert test_leads[0].created_at > test_leads[1].created_at > test_leads[2].created_at


# Test for PaymentsToWeb model
@pytest.mark.django_db
def test_payments_to_web_field_verbose_name(create_user, create_web, create_payment_to_web):
    test_user = create_user()
    test_web = create_web()
    test_payment = create_payment_to_web(web=test_web, user_added=test_user)
    assert test_payment._meta.get_field('web_FK').verbose_name == 'Web FK'
    assert test_payment._meta.get_field('payment_amount').verbose_name == 'Amount paid'
    assert test_payment._meta.get_field('payment_date').verbose_name == 'Payment date and time'
    assert test_payment._meta.get_field('user_added').verbose_name == 'Added by existing user (login)'


@pytest.mark.django_db
def test_payments_to_web_field_payment_amount_max_digits_decimal_places_and_validators(create_user, create_web,
                                                                                       create_payment_to_web):
    test_user = create_user()
    test_web = create_web()
    test_payment = create_payment_to_web(web=test_web, user_added=test_user)
    assert test_payment._meta.get_field('payment_amount').max_digits == 10
    assert test_payment._meta.get_field('payment_amount').decimal_places == 2
    assert test_payment._meta.get_field('payment_amount').validators[0] == MinValueValidator(0)


@pytest.mark.django_db
def test_payments_to_web_str_method(create_user, create_web, create_payment_to_web):
    test_user = create_user()
    test_web = create_web()
    test_payment = create_payment_to_web(web=test_web, user_added=test_user)
    assert str(test_payment) == f'{test_payment.web_FK}, {test_payment.payment_amount}'


# Test for Order model
@pytest.mark.django_db
def test_order_field_verbose_name(create_order):
    test_order = create_order()
    assert test_order._meta.get_field('order_created').verbose_name == 'Order created date and time'
    assert test_order._meta.get_field('lead_FK').verbose_name == 'Lead FK'
    assert test_order._meta.get_field('customer_first_name').verbose_name == 'Customer first name'
    assert test_order._meta.get_field('customer_last_name').verbose_name == 'Customer last name'
    assert test_order._meta.get_field('status').verbose_name == 'Order status'
    assert test_order._meta.get_field('sent_date').verbose_name == 'Send date for the order'
    assert test_order._meta.get_field('contact_phone').verbose_name == 'Contact phone'
    assert test_order._meta.get_field('delivery_city').verbose_name == 'Delivery city'
    assert test_order._meta.get_field('delivery_street').verbose_name == 'Delivery street'
    assert test_order._meta.get_field('delivery_house_number').verbose_name == 'Delivery house number'
    assert test_order._meta.get_field('delivery_apartment_number').verbose_name == 'Delivery apartment number'
    assert test_order._meta.get_field('delivery_zip_code').verbose_name == 'Delivery zip code'
    assert test_order._meta.get_field('order_operator').verbose_name == 'Operator FK'


@pytest.mark.django_db
def test_order_field_max_length(create_order):
    test_order = create_order()
    assert test_order._meta.get_field('customer_first_name').max_length == 25
    assert test_order._meta.get_field('customer_last_name').max_length == 25
    assert test_order._meta.get_field('status').max_length == 30
    assert test_order._meta.get_field('contact_phone').max_length == 11
    assert test_order._meta.get_field('delivery_city').max_length == 30
    assert test_order._meta.get_field('delivery_street').max_length == 30
    assert test_order._meta.get_field('delivery_house_number').max_length == 30
    assert test_order._meta.get_field('delivery_apartment_number').max_length == 30
    assert test_order._meta.get_field('delivery_zip_code').max_length == 5


@pytest.mark.django_db
def test_order_null_false_fields(create_order):
    test_order = create_order()
    assert not test_order._meta.get_field('customer_first_name').null
    assert not test_order._meta.get_field('customer_last_name').null
    assert not test_order._meta.get_field('status').null
    assert not test_order._meta.get_field('sent_date').null
    assert not test_order._meta.get_field('contact_phone').null
    assert not test_order._meta.get_field('delivery_city').null
    assert not test_order._meta.get_field('delivery_street').null
    assert not test_order._meta.get_field('delivery_zip_code').null


@pytest.mark.django_db
def test_order_str_method(create_order):
    test_order = create_order()
    assert str(test_order) == f'Order {test_order.pk}'


@pytest.mark.django_db
def test_order_ordering(create_order):
    for _ in range(3):
        create_order()
    test_orders = Order.objects.all()
    assert test_orders[0].order_created > test_orders[1].order_created > test_orders[2].order_created


# Test for OrderedProduct model
@pytest.mark.django_db
def test_ordered_product_field_verbose_name(create_ordered_product):
    test_ordered_product = create_ordered_product()
    assert test_ordered_product._meta.get_field('order_FK').verbose_name == 'Order FK'
    assert test_ordered_product._meta.get_field('product_FK').verbose_name == 'Product FK'
    assert test_ordered_product._meta.get_field('ordered_quantity').verbose_name == 'Ordered quantity'
    assert test_ordered_product._meta.get_field('ordered_product_price').verbose_name == 'Ordered product total price'


@pytest.mark.django_db
def test_ordered_product_max_digits_decimal_places_validators(create_ordered_product):
    test_ordered_product = create_ordered_product()
    assert test_ordered_product._meta.get_field('ordered_quantity').validators[0] == MinValueValidator(0)
    assert test_ordered_product._meta.get_field('ordered_product_price').validators[0] == MinValueValidator(0)
    assert test_ordered_product._meta.get_field('ordered_product_price').max_digits == 10
    assert test_ordered_product._meta.get_field('ordered_product_price').decimal_places == 2


@pytest.mark.django_db
def test_ordered_product_str_method(create_order, create_product_category, create_product, create_ordered_product):
    test_order = create_order()
    test_product_category = create_product_category()
    test_product = create_product(test_product_category)
    test_ordered_product_with_order_and_product = create_ordered_product(order=test_order, product=test_product)
    test_ordered_product_no_order_no_product = create_ordered_product()
    assert str(test_ordered_product_with_order_and_product) == f'{test_ordered_product_with_order_and_product.order_FK}:'\
                                                               f' {test_ordered_product_with_order_and_product.product_FK}' \
                                                               f' - {test_ordered_product_with_order_and_product.ordered_quantity}'
    assert str(test_ordered_product_no_order_no_product) == f'Deleted order: Deleted product - ' \
                                                            f'{test_ordered_product_no_order_no_product.ordered_quantity}'


@pytest.mark.django_db
def test_ordered_product_total_price_method(create_ordered_product):
    price = 5.5
    ordered_quantity = 3
    test_ordered_product = create_ordered_product(ordered_product_price=price, ordered_quantity=ordered_quantity)
    assert test_ordered_product.total_price() == float(price) * float(ordered_quantity)
