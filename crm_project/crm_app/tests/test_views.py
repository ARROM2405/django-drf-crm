import pprint
from unittest import mock

import pytest
from django.contrib import auth
from django.core.files import File
from django.shortcuts import reverse
from crm_app.tests.fixtures import *
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse_lazy


# Permissions
def permission_create_lead():
    ct = ContentType.objects.get(app_label='crm_app', model='lead')
    perm = Permission.objects.get(codename='add_lead')
    if perm:
        return perm
    perm = Permission.objects.create(codename='add_lead', name='can add lead', content_type=ct)
    return perm


def permission_view_lead():
    ct = ContentType.objects.get(app_label='crm_app', model='lead')
    perm = Permission.objects.get(codename='view_lead')
    if perm:
        return perm
    perm = Permission.objects.create(codename='view_lead', name='can view lead', content_type=ct)
    return perm


def permission_create_product_category():
    ct = ContentType.objects.get(app_label='crm_app', model='productcategory')
    if Permission.objects.get(codename='add_productcategory'):
        return Permission.objects.get(codename='add_productcategory')
    perm = Permission.objects.create(codename='add_productcategory', name='can add product category',
                                     content_type=ct)
    return perm


def permission_create_order():
    ct = ContentType.objects.get(app_label='crm_app', model='order')
    if Permission.objects.get(codename='add_order'):
        return Permission.objects.get(codename='add_order')
    perm = Permission.objects.create(codename='add_order', name='can add order',
                                     content_type=ct)
    return perm


def permission_view_order():
    ct = ContentType.objects.get(app_label='crm_app', model='order')
    if Permission.objects.get(codename='view_order'):
        return Permission.objects.get(codename='view_order')
    perm = Permission.objects.create(codename='view_order', name='can view order',
                                     content_type=ct)
    return perm


def permission_change_order():
    ct = ContentType.objects.get(app_label='crm_app', model='order')
    if Permission.objects.get(codename='change_order'):
        return Permission.objects.get(codename='change_order')
    perm = Permission.objects.create(codename='change_order', name='can change order',
                                     content_type=ct)
    return perm


def permission_create_web():
    return Permission.objects.get(codename='add_web')


def permission_view_web():
    return Permission.objects.get(codename='view_web')


def permission_change_web():
    return Permission.objects.get(codename='change_web')


def permission_create_payment():
    return Permission.objects.get(codename='add_paymentstoweb')


def permission_view_payment():
    return Permission.objects.get(codename='view_paymentstoweb')


def permission_change_payment():
    return Permission.objects.get(codename='change_paymentstoweb')


def permission_view_product_category():
    return Permission.objects.get(codename='view_productcategory')


def permission_create_product_category():
    return Permission.objects.get(codename='add_productcategory')


def permission_change_product_category():
    return Permission.objects.get(codename='change_productcategory')


def permission_create_product():
    return Permission.objects.get(codename='add_product')


def permission_view_product():
    return Permission.objects.get(codename='view_product')


def permission_change_product():
    return Permission.objects.get(codename='change_product')


def permission_create_offer():
    return Permission.objects.get(codename='add_offer')


def permission_view_offer():
    return Permission.objects.get(codename='view_offer')


def permission_change_offer():
    return Permission.objects.get(codename='change_offer')


def permission_view_profile():
    return Permission.objects.get(codename='view_profile')


# Tests for RegisterView
@pytest.mark.django_db
def test_url_get_request_register_view(client):
    url = reverse('register')
    assert client.get(url).status_code == 200


@pytest.mark.django_db
def test_template_used_register_view(client):
    url = reverse('register')
    response = client.get(url)
    assert 'crm_app/registration.html' in (t.name for t in response.templates)


@pytest.mark.django_db
def test_redirect_url_for_successful_registration_register_view(client):
    url = reverse('register')
    redirect_url = reverse_lazy('home_page', kwargs={'stat': 'prod'})
    data = {'username': 'test_username',
            'password1': 'test_password',
            'password2': 'test_password'}

    response = client.post(url, data=data)
    assert response.status_code == 302
    assert response['Location'] == redirect_url


# Tests for UserLoginView
@pytest.mark.django_db
def test_url_get_request_user_login_view(client):
    url = reverse('login')
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_template_used_login_view(client):
    url = reverse('login')
    response = client.get(url)
    assert 'crm_app/login.html' in (t.name for t in response.templates)


@pytest.mark.django_db
def test_successful_login_user_login_view(client, create_user):
    test_client = client
    test_username = 'test_user'
    test_password = 'test_password'
    test_user = create_user(username=test_username, password=test_password)
    data = {'id_username': test_username, 'id_password': test_password}
    login_url = reverse('login')
    post_login_response = test_client.post(login_url, data=data)
    assert post_login_response.status_code == 200


# Tests for HomePageView
@pytest.mark.django_db
def test_template_used_home_page_view(client, create_profile):
    url = reverse('home_page', kwargs={'stat': 'prod'})
    test_password = 'test_password'
    test_profile = create_profile(password=test_password)
    client.login(username=test_profile.user.username, password=test_password)
    response = client.get(url)
    assert response.status_code == 200
    assert 'crm_app/home_page.html' in (t.name for t in response.templates)


@pytest.mark.django_db
def test_get_request_for_not_authenticated_user_home_page_view(client):
    url = reverse('home_page', kwargs={'stat': 'prod'})
    redirect_url = reverse('login')
    response = client.get(url)
    assert response.status_code == 302
    assert redirect_url in response['Location']


@pytest.mark.django_db
def test_get_request_for_authenticated_user_home_page_view(create_profile, client):
    url = reverse('home_page', kwargs={'stat': 'prod'})
    test_username = 'test_user'
    test_password = 'test_password'
    user = create_profile(username=test_username, password=test_password)
    client.login(username=test_username, password=test_password)
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_menu_items_on_home_page_for_operator_role(create_profile, client):
    test_password = 'password_operator'
    url = reverse('home_page', kwargs={'stat': 'prod'})
    operator_profile = create_profile(username='username_operator', password=test_password, role='Operator')
    client.login(username=operator_profile.user.username, password=test_password)
    response = client.get(url)
    assert response.status_code == 200
    for item in ['Offers', 'Payments', 'Users']:
        assert item not in str(response.content)


@pytest.mark.django_db
def test_menu_items_on_home_page_for_stock_manager_role(create_profile, client):
    test_password = 'password_stock_manager'
    url = reverse('home_page', kwargs={'stat': 'prod'})
    stock_manager_profile = create_profile(username='username_stock_manager', password=test_password,
                                           role='Stock manager')
    print(stock_manager_profile.user.username, stock_manager_profile.user.password)
    client.login(username=stock_manager_profile.user.username, password=test_password)
    response = client.get(url)
    assert response.status_code == 200
    for item in ['Leads', 'Orders', 'Offers', 'Payments', 'Users']:
        assert item not in str(response.content)


@pytest.mark.django_db
def test_menu_items_on_home_page_for_payments_executive_role(create_profile, client):
    test_password = 'password_payments_executive'
    url = reverse('home_page', kwargs={'stat': 'prod'})
    payments_executive_profile = create_profile(username='username_payments_executive',
                                                password=test_password, role='Payments executive')
    client.login(username=payments_executive_profile.user.username, password=test_password)
    response = client.get(url)
    assert response.status_code == 200
    for item in ['Leads', 'Orders', 'Users']:
        assert item not in str(response.content)


@pytest.mark.django_db
def test_menu_items_on_home_page_for_administrator_role(create_profile, client):
    test_password = 'password_administrator'
    url = reverse('home_page', kwargs={'stat': 'prod'})
    administrator_profile = create_profile(username='username_administrator', password=test_password,
                                           role='Administrator')
    client.login(username=administrator_profile.user.username, password=test_password)
    response = client.get(url)
    assert response.status_code == 200
    for item in ['Main', 'Product categories', 'Products', 'Leads', 'Orders', 'Webs', 'Offers', 'Payments', 'Users']:
        assert item in str(response.content)


# Tests for LogoutView
@pytest.mark.django_db
def test_logout_view_redirect_page(create_profile, client):
    test_password = 'test_password'
    test_profile = create_profile(password=test_password)
    client.login(usename=test_profile.user.username, password=test_password)
    response = client.get(reverse('logout'))
    assert response.status_code == 302
    assert reverse('login') in response['Location']


# Tests for LeadCreationView
@pytest.mark.django_db
def test_template_used_lead_creation_view(admin_client):
    url = reverse('lead_creation')
    response = admin_client.get(url)
    assert 'crm_app/lead_creation.html' in (t.name for t in response.templates)


@pytest.mark.django_db
def test_get_request_unauthorized_user_lead_creation(client):
    url = reverse('lead_creation')
    response = client.get(url)
    assert response.status_code == 302
    assert reverse('login') in response['Location']


@pytest.mark.django_db
def test_get_request_no_permission_lead_creation(create_profile, client):
    test_password = 'test_password'
    test_profile = create_profile(password=test_password)
    client.login(username=test_profile.user.username, password=test_password)
    response = client.get(reverse('lead_creation'))
    assert response.status_code == 403


@pytest.mark.django_db
def test_get_request_has_permission_lead_creation(create_profile, client):
    url = reverse('lead_creation')
    test_password = 'test_password'
    test_user = create_profile(password=test_password, perm=[permission_create_lead()])
    client.login(username=test_user.user.username, password=test_password)
    response = client.get(url)
    assert response.status_code == 200


# TODO: test not working properly
@pytest.mark.xfail
@pytest.mark.django_db
def test_post_request_redirect_url_and_lead_cost_lead_creation(create_profile, create_product_category, create_product,
                                                               create_web, create_offer, client):
    testing_url = reverse('lead_creation')
    redirect_url = reverse('lead_list')
    test_password = 'test_password'
    test_profile = create_profile(password=test_password, perm=[permission_create_lead()])
    test_product_category = create_product_category()
    test_product = create_product(product_category=test_product_category)
    test_web = create_web()
    test_offer = create_offer(product=test_product, web=test_web)
    client.login(username=test_profile.user.username, password=test_password)
    offer_fk = test_offer.pk
    contact_phone = '111-111-111'
    customer_fn = 'test_fn'
    customer_ln = 'test_ln'
    response = client.post(testing_url, data={'offer_FK': test_offer.pk,
                                              'contact_phone:': contact_phone,
                                              'customer_first_n˜ame': customer_fn,
                                              'customer_last_name': customer_ln},
                           )
    pprint.pprint(response.content)
    assert response.status_code == 302
    assert response['Location'] == redirect_url
    assert Lead.objects.all().first().lead_cost == test_offer.lead_cost


# Tests for LeadDetailView
@pytest.mark.django_db
def test_template_used_lead_detail_view(admin_client, create_product_category, create_product, create_web, create_offer,
                                        create_lead):
    test_product_category = create_product_category()
    test_product = create_product(product_category=test_product_category)
    test_web = create_web()
    test_offer = create_offer(product=test_product, web=test_web)
    test_lead = create_lead(offer=test_offer)
    url = reverse('lead_detail', kwargs={'id': test_lead.pk})
    response = admin_client.get(url)
    assert 'crm_app/lead_detail.html' in (t.name for t in response.templates)


@pytest.mark.django_db
def test_unauthorised_user_get_request_lead_detail(client, create_profile, create_product_category, create_product,
                                                   create_web, create_offer, create_lead):
    # test_password = 'test_password'
    # test_profile = create_profile(password=test_password, perm=[permission_view_lead()])
    test_product_category = create_product_category()
    test_product = create_product(product_category=test_product_category)
    test_web = create_web()
    test_offer = create_offer(product=test_product, web=test_web)
    test_lead = create_lead(offer=test_offer)
    # client.login(username=test_profile.user.username, password=test_password)
    response = client.get(reverse('lead_detail', kwargs={'id': test_lead.pk}))
    assert response.status_code == 302
    assert reverse('login') in response['Location']


@pytest.mark.django_db
def test_no_permission_get_request_lead_detail(client, create_profile, create_product_category, create_product,
                                               create_web, create_offer, create_lead):
    test_password = 'test_password'
    test_profile = create_profile(password=test_password)
    test_product_category = create_product_category()
    test_product = create_product(product_category=test_product_category)
    test_web = create_web()
    test_offer = create_offer(product=test_product, web=test_web)
    test_lead = create_lead(offer=test_offer)
    client.login(username=test_profile.user.username, password=test_password)
    response = client.get(reverse('lead_detail', kwargs={'id': test_lead.pk}))
    assert response.status_code == 403


@pytest.mark.django_db
def test_has_permission_get_request_lead_detail(client, create_profile, create_product_category, create_product,
                                                create_web, create_offer, create_lead):
    test_password = 'test_password'
    test_profile = create_profile(password=test_password, perm=[permission_view_lead()])
    test_product_category = create_product_category()
    test_product = create_product(product_category=test_product_category)
    test_web = create_web()
    test_offer = create_offer(product=test_product, web=test_web)
    test_lead = create_lead(offer=test_offer)
    client.login(username=test_profile.user.username, password=test_password)
    response = client.get(reverse('lead_detail', kwargs={'id': test_lead.pk}))
    assert response.status_code == 200
    assert 'Create order' not in str(response.content)
    test_profile.user.user_permissions.add(permission_create_order())
    response_added_create_order_permission = client.get(reverse('lead_detail', kwargs={'id': test_lead.pk}))
    assert 'Create order' in str(response_added_create_order_permission.content)


@pytest.mark.django_db
def test_template_and_url_lead_detail_view(client, create_profile, create_product_category, create_product, create_web,
                                           create_offer, create_lead):
    test_password = 'test_password'
    test_profile = create_profile(password=test_password, perm=[permission_view_lead()])
    test_product_category = create_product_category()
    test_product = create_product(product_category=test_product_category)
    test_web = create_web()
    test_offer = create_offer(product=test_product, web=test_web)
    test_lead = create_lead(offer=test_offer)
    url = reverse('lead_detail', kwargs={'id': test_lead.pk})
    client.login(username=test_profile.user.username, password=test_password)
    response = client.get(url)
    assert response.status_code == 200
    assert 'crm_app/lead_detail.html' in [t.name for t in response.templates]


@pytest.mark.django_db
def test_order_create_button_according_to_permission_lead_detail_view(client, create_profile, create_product_category,
                                                                      create_product, create_web, create_offer,
                                                                      create_lead):
    test_password = 'test_password'
    test_profile = create_profile(password=test_password, perm=[permission_view_lead()])
    test_product_category = create_product_category()
    test_product = create_product(product_category=test_product_category)
    test_web = create_web()
    test_offer = create_offer(product=test_product, web=test_web)
    test_lead = create_lead(offer=test_offer)
    url = reverse('lead_detail', kwargs={'id': test_lead.pk})
    client.login(username=test_profile.user.username, password=test_password)
    no_permission_response = client.get(url)
    assert no_permission_response.status_code == 200
    assert 'Create order' not in str(no_permission_response.content)
    test_profile.user.user_permissions.add(permission_create_order())
    permission_response = client.get(url)
    assert permission_response.status_code == 200
    assert 'Create order' in str(permission_response.content)


# Tests for LeadListView
@pytest.mark.django_db
def test_template_used_and_url_lead_list_view(client, create_profile):
    test_password = 'test_password'
    test_profile = create_profile(password=test_password, perm=[permission_view_lead()])
    url = reverse('lead_list')
    client.login(username=test_profile.user.username, password=test_password)
    response = client.get(url)
    assert response.status_code == 200
    assert 'crm_app/lead_list.html' in (t.name for t in response.templates)


@pytest.mark.django_db
def test_add_lead_button_according_to_permissions_lead_list_view(client, create_profile):
    url = reverse('lead_list')
    test_password = 'test_password'
    permission_username = 'permission_username'
    no_permission_username = 'no_permission_username'
    permission_profile = create_profile(username=permission_username, password=test_password,
                                        perm=[permission_create_lead(), permission_view_lead()])
    client.login(username=permission_username, password=test_password)
    permission_response = client.get(url)
    assert permission_response.status_code == 200
    assert 'Add lead' in str(permission_response.content)
    client.logout()
    no_permission_profile = create_profile(username=no_permission_username, password=test_password,
                                           perm=[permission_view_lead()])
    client.login(username=no_permission_username, password=test_password)
    no_permission_response = client.get(url)
    assert no_permission_response.status_code == 200
    assert 'Add lead' not in str(no_permission_response.content)


# Tests for OrderCreationView
@pytest.mark.django_db
def test_url_and_template_for_order_create_view(client, create_profile):
    test_password = 'test_password'
    test_profile = create_profile(password=test_password, perm=[permission_create_order()])
    url = reverse('order_creation')
    client.login(username=test_profile.user.username, password=test_password)
    response = client.get(url)
    assert response.status_code == 200
    assert 'crm_app/order_creation.html' in [t.name for t in response.templates]


@pytest.mark.django_db
def test_successful_post_request_order_create_view(client, create_profile, create_product_category, create_product):
    test_password = 'test_password'
    url = reverse('order_creation')
    test_profile = create_profile(password=test_password, perm=[permission_create_order(), permission_view_order()])
    test_product_category = create_product_category()
    test_product = create_product(product_category=test_product_category)
    ordered_products_quantity = 2
    ordered_products_price = 10.5
    client.login(username=test_profile.user.username, password=test_password)
    post_data = {
        'customer_first_name': 'test_fn',
        'customer_last_name': 'test_ln',
        'status': 'New order',
        'sent_date': '2022-07-01',
        'contact_phone': '111-111-111',
        'delivery_city': 'test_city',
        'delivery_street': 'test_street',
        'delivery_house_number': '1',
        'delivery_zip_code': '11111',
        'product_1': test_product.pk,
        'product_1_quantity': ordered_products_quantity,
        'product_1_price': ordered_products_price
    }
    response = client.post(url, data=post_data)
    assert response.status_code == 302
    assert len(Order.objects.all()) == 1
    assert Order.objects.all().first().order_operator == test_profile.user
    assert OrderedProduct.objects.get(order_FK=Order.objects.all().first()).total_price() == \
           ordered_products_quantity * ordered_products_price


# Tests for OrderDetailView
@pytest.mark.django_db
def test_url_and_template_for_order_detail_view(client, create_order, create_product, create_product_category,
                                                create_ordered_product, create_profile):
    test_order = create_order()
    test_password = 'test_password'
    test_profile = create_profile(password=test_password, perm=[permission_view_order()])
    client.login(username=test_profile.user.username, password=test_password)
    url = reverse('order_detail', kwargs={'id': test_order.pk})
    response = client.get(url)
    assert response.status_code == 200
    assert 'crm_app/order_detail.html' in [t.name for t in response.templates]


@pytest.mark.django_db
def test_no_permission_get_request_order_detail_view(client, create_profile, create_order):
    test_order = create_order()
    url = reverse('order_detail', kwargs={'id': test_order.pk})
    test_password = 'test_password'
    test_profile = create_profile(password=test_password)
    client.login(username=test_profile.user.username, password=test_password)
    response = client.get(url)
    assert response.status_code == 403


@pytest.mark.django_db
def test_update_button_order_detail_view(client, create_profile, create_order):
    test_password = 'test_profile'
    test_profile = create_profile(password=test_password, perm=[permission_view_order()])
    test_order = create_order()
    url = reverse('order_detail', kwargs={'id': test_order.pk})
    client.login(username=test_profile.user.username, password=test_password)
    response = client.get(url)
    assert response.status_code == 200
    assert 'Update order' not in str(response.content)
    client.logout()
    test_profile.user.user_permissions.add(permission_change_order())
    client.login(username=test_profile.user.username, password=test_password)
    response = client.get(url)
    assert response.status_code == 200
    assert 'Update order' in str(response.content)


# Tests for OrderListView
@pytest.mark.django_db
def test_url_and_template_for_order_list_view(client, create_profile):
    url = reverse('order_list')
    test_password = 'test_password'
    test_profile = create_profile(password=test_password, perm=[permission_view_order()])
    client.login(username=test_profile.user.username, password=test_password)
    response = client.get(url)
    assert response.status_code == 200
    assert 'crm_app/order_list.html' in [t.name for t in response.templates]


@pytest.mark.django_db
def test_no_permission_get_request_order_list_view(client, create_profile):
    url = reverse('order_list')
    test_password = 'test_password'
    test_profile = create_profile(password=test_password)
    client.login(username=test_profile.user.username, password=test_password)
    response = client.get(url)
    assert response.status_code == 403


# Tests for OrderUpdateView
@pytest.mark.django_db
def test_url_and_template_for_order_update_view(client, create_order, create_profile):
    test_order = create_order()
    url = reverse('order_update', kwargs={'id': test_order.pk})
    test_password = 'test_password'
    test_profile = create_profile(password=test_password, perm=[permission_change_order()])
    client.login(username=test_profile.user.username, password=test_password)
    response = client.get(url)
    assert response.status_code == 200
    assert 'crm_app/order_update.html' in [t.name for t in response.templates]


@pytest.mark.django_db
def test_no_permission_get_request_order_update_view(client, create_profile, create_order):
    test_order = create_order()
    url = reverse('order_update', kwargs={'id': test_order.pk})
    test_password = 'test_password'
    test_profile = create_profile(password=test_password)
    client.login(username=test_profile.user.username, password=test_password)
    response = client.get(url)
    assert response.status_code == 403


@pytest.mark.django_db
def test_successful_post_request_order_update_view(client, create_profile, create_order, create_product_category,
                                                   create_product, create_ordered_product):
    test_product_category = create_product_category()
    ordered_quantity = 5
    quantity_in_stock = 10
    test_product = create_product(product_category=test_product_category, quantity_available=quantity_in_stock,
                                  quantity_in_delivery=ordered_quantity)
    test_order = create_order()
    test_ordered_product = create_ordered_product(order=test_order, product=test_product,
                                                  ordered_quantity=ordered_quantity)
    url = reverse('order_update', kwargs={'id': test_order.pk})
    test_password = 'test_password'
    test_profile = create_profile(password=test_password, perm=[permission_change_order()])
    client.login(username=test_profile.user.username, password=test_password)
    post_data = {
        'status': 'Delivered',
        'sent_date': datetime.datetime.now().date(),
        'contact_phone': '111-111-111',
        'delivery_city': 'updated_delivery_city',
        'delivery_street': 'test_delivery_street',
        'delivery_zip_code': '11111'
    }
    assert Order.objects.get(pk=test_order.pk).status == 'New order'
    assert Order.objects.get(pk=test_order.pk).delivery_city == 'test_city'
    assert Product.objects.get(pk=test_product.pk).quantity_in_delivery == ordered_quantity
    response = client.post(url, data=post_data)
    assert response.status_code == 302
    assert Order.objects.get(pk=test_order.pk).status == 'Delivered'
    assert Order.objects.get(pk=test_order.pk).delivery_city == 'updated_delivery_city'
    assert Product.objects.get(pk=test_product.pk).quantity_in_delivery == 0
    assert Product.objects.get(pk=test_product.pk).quantity_available == quantity_in_stock
    post_data['status'] = 'Sent'
    response = client.post(url, data=post_data)
    assert response.status_code == 302
    assert Product.objects.get(pk=test_product.pk).quantity_in_delivery == ordered_quantity
    post_data['status'] = 'Return'
    response = client.post(url, data=post_data)
    assert response.status_code == 302
    assert Product.objects.get(pk=test_product.pk).quantity_in_delivery == 0
    assert Product.objects.get(pk=test_product.pk).quantity_available == quantity_in_stock + ordered_quantity


# Tests for WebCreationView
@pytest.mark.django_db
def test_url_and_template_for_web_create_view(client, create_profile):
    url = reverse('web_creation')
    test_password = 'test_password'
    test_profile = create_profile(password=test_password, perm=[permission_create_web()])
    client.login(username=test_profile.user.username, password=test_password)
    response = client.get(url)
    assert response.status_code == 200
    assert 'crm_app/web_creation.html' in [t.name for t in response.templates]


@pytest.mark.django_db
def test_no_permission_get_request_web_create_view(client, create_profile):
    url = reverse('web_creation')
    test_password = 'test_password'
    test_profile = create_profile(password=test_password)
    client.login(username=test_profile.user.username, password=test_password)
    response = client.get(url)
    assert response.status_code == 403


@pytest.mark.django_db
def test_successful_post_request_web_create_view(client, create_profile):
    url = reverse('web_creation')
    test_password = 'test_password'
    test_profile = create_profile(password=test_password, perm=[permission_create_web()])
    client.login(username=test_profile.user.username, password=test_password)
    web_name = 'test_web'
    web_description = 'test_description'
    web_balance = 100
    post_data = {
        'web_name': web_name,
        'web_description': web_description,
        'web_api_key': 'test_api_key',
        'balance': web_balance
    }
    response = client.post(url, data=post_data)
    web_created = Web.objects.all().first()

    assert response.status_code == 302
    assert web_created.web_name == web_name
    assert web_created.web_description == web_description
    assert web_created.balance == web_balance


# Tests for WebDetailView
@pytest.mark.django_db
def test_url_and_template_for_web_detail_view(client, create_profile, create_web):
    test_web = create_web()
    url = reverse('web_detail', kwargs={'id': test_web.pk})
    test_password = 'test_password'
    test_profile = create_profile(password=test_password, perm=[permission_view_web()])
    client.login(username=test_profile.user.username, password=test_password)
    response = client.get(url)
    assert response.status_code == 200
    assert 'crm_app/web_detail.html' in [t.name for t in response.templates]


@pytest.mark.django_db
def test_no_permission_get_request_web_detail_view(client, create_profile, create_web):
    test_web = create_web()
    url = reverse('web_detail', kwargs={'id': test_web.pk})
    test_password = 'test_password'
    test_profile = create_profile(password=test_password)
    client.login(username=test_profile.user.username, password=test_password)
    response = client.get(url)
    assert response.status_code == 403


@pytest.mark.dajngo_db
def test_update_web_button_permissions_web_detail_view(client, create_profile, create_web):
    test_web = create_web()
    url = reverse('web_detail', kwargs={'id': test_web.pk})
    test_password = 'test_password'
    test_profile = create_profile(password=test_password, perm=[permission_view_web()])
    client.login(username=test_profile.user.username, password=test_password)
    response_no_permission = client.get(url)
    assert response_no_permission.status_code == 200
    assert 'Update web' not in str(response_no_permission.content)
    client.logout()
    test_profile.user.user_permissions.add(permission_change_web())
    client.login(username=test_profile.user.username, password=test_password)
    response_has_permission = client.get(url)
    assert response_has_permission.status_code == 200
    assert 'Update web' in str(response_has_permission.content)


# Tests for WebListView
@pytest.mark.django_db
def test_url_and_template_for_web_list_view(client, create_profile):
    url = reverse('web_list')
    test_password = 'test_password'
    test_profile = create_profile(password=test_password, perm=[permission_view_web()])
    client.login(username=test_profile.user.username, password=test_password)
    response = client.get(url)
    assert response.status_code == 200
    assert 'crm_app/web_list.html' in [t.name for t in response.templates]


@pytest.mark.django_db
def test_no_permission_get_request_web_list_view(client, create_profile):
    url = reverse('web_list')
    test_password = 'test_password'
    test_profile = create_profile(password=test_password)
    client.login(username=test_profile.user.username, password=test_password)
    response = client.get(url)
    assert response.status_code == 403


@pytest.mark.dajngo_db
def test_add_new_web_button_permissions_web_list_view(client, create_profile):
    url = reverse('web_list')
    test_password = 'test_password'
    test_profile = create_profile(password=test_password, perm=[permission_view_web()])
    client.login(username=test_profile.user.username, password=test_password)
    response_no_permission = client.get(url)
    assert response_no_permission.status_code == 200
    assert 'Add new web' not in str(response_no_permission.content)
    client.logout()
    test_profile.user.user_permissions.add(permission_create_web())
    client.login(username=test_profile.user.username, password=test_password)
    response_has_permission = client.get(url)
    assert response_has_permission.status_code == 200
    assert 'Add new web' in str(response_has_permission.content)


# Tests for WebUpdateView
@pytest.mark.django_db
def test_url_and_template_for_web_list_view(client, create_profile, create_web):
    test_web = create_web()
    url = reverse('web_update', kwargs={'id': test_web.pk})
    test_password = 'test_password'
    test_profile = create_profile(password=test_password, perm=[permission_change_web()])
    client.login(username=test_profile.user.username, password=test_password)
    response = client.get(url)
    assert response.status_code == 200
    assert 'crm_app/web_update.html' in [t.name for t in response.templates]


@pytest.mark.django_db
def test_no_permission_get_request_web_update_view(client, create_profile, create_web):
    test_web = create_web()
    url = reverse('web_update', kwargs={'id': test_web.pk})
    test_password = 'test_password'
    test_profile = create_profile(password=test_password)
    client.login(username=test_profile.user.username, password=test_password)
    response = client.get(url)
    assert response.status_code == 403


@pytest.mark.django_db
def test_successful_post_request_web_update_view(client, create_profile, create_web):
    original_web_name = 'test_web'
    updated_web_name = 'updated_web_name'
    original_web_description = 'test_description'
    updated_web_description = 'updated_web_description'
    original_web_status = True
    updated_web_status = False
    test_web = create_web(web_name=original_web_name, web_description=original_web_description)
    url = reverse('web_update', kwargs={'id': test_web.pk})
    test_password = 'test_password'
    test_profile = create_profile(password=test_password, perm=[permission_change_web()])
    client.login(username=test_profile.user.username, password=test_password)
    post_data = {
        'web_name': updated_web_name,
        'web_description': updated_web_description,
        'active': updated_web_status
    }
    original_web = Web.objects.all().first()
    assert original_web.web_name == original_web_name
    assert original_web.web_description == original_web_description
    assert original_web.active == original_web_status
    response = client.post(url, data=post_data)
    updated_web = Web.objects.all().first()
    assert response.status_code == 302
    assert updated_web.web_name == updated_web_name
    assert updated_web.web_description == updated_web_description
    assert updated_web.active == updated_web_status


# Tests for PaymentCreationView
@pytest.mark.django_db
def test_url_and_template_for_payments_creation_view(client, create_profile, create_web):
    test_web = create_web()
    url = reverse('payment_creation', kwargs={'web_id': test_web.pk})
    test_password = 'test_password'
    test_profile = create_profile(password=test_password, perm=[permission_create_payment()])
    client.login(username=test_profile.user.username, password=test_password)
    response = client.get(url)
    assert response.status_code == 200
    assert 'crm_app/payment_creation.html' in [t.name for t in response.templates]


@pytest.mark.django_db
def test_no_permission_get_request_payments_create_view(client, create_profile, create_web):
    test_web = create_web()
    url = reverse('payment_creation', kwargs={'web_id': test_web.pk})
    test_password = 'test_password'
    test_profile = create_profile(password=test_password)
    client.login(username=test_profile.user.username, password=test_password)
    response = client.get(url)
    assert response.status_code == 403


@pytest.mark.django_db
def test_successful_post_request_web_update_view(client, create_profile, create_web):
    original_balance = 50
    payment_amount = 10
    test_web = create_web(balance=original_balance)
    url = reverse('payment_creation', kwargs={'web_id': test_web.pk})
    test_password = 'test_password'
    test_profile = create_profile(password=test_password, perm=[permission_create_payment()])
    client.login(username=test_profile.user.username, password=test_password)
    post_data = {
        'web_FK': test_web.pk,
        'payment_amount': payment_amount
    }
    assert test_web.balance == original_balance
    response = client.post(url, data=post_data)
    assert response.status_code == 302
    test_web = Web.objects.all().first()
    assert test_web.balance == original_balance - payment_amount


# Tests for PaymentDetailView
@pytest.mark.django_db
def test_url_and_template_for_payments_detail_view(client, create_profile, create_web, create_payment_to_web):
    test_password = 'test_password'
    test_profile = create_profile(password=test_password, perm=[permission_view_payment()])
    test_web = create_web()
    test_payment = create_payment_to_web(web=test_web, user_added=test_profile.user)
    url = reverse('payment_detail', kwargs={'id': test_payment.pk})
    client.login(username=test_profile.user.username, password=test_password)
    response = client.get(url)
    assert response.status_code == 200
    assert 'crm_app/payment_detail.html' in [t.name for t in response.templates]


@pytest.mark.django_db
def test_no_permission_get_request_payments_detail_view(client, create_profile, create_web, create_payment_to_web):
    test_password = 'test_password'
    test_profile = create_profile(password=test_password)
    test_web = create_web()
    test_payment = create_payment_to_web(web=test_web, user_added=test_profile.user)
    url = reverse('payment_detail', kwargs={'id': test_payment.pk})
    client.login(username=test_profile.user.username, password=test_password)
    response = client.get(url)
    assert response.status_code == 403


@pytest.mark.django_db
def test_button_permission_payment_detail_view(client, create_profile, create_web, create_payment_to_web):
    test_password = 'test_password'
    test_profile = create_profile(password=test_password, perm=[permission_view_payment()])
    test_web = create_web()
    test_payment = create_payment_to_web(web=test_web, user_added=test_profile.user)
    url = reverse('payment_detail', kwargs={'id': test_payment.pk})
    client.login(username=test_profile.user.username, password=test_password)
    response_no_permission = client.get(url)
    assert response_no_permission.status_code == 200
    assert 'Update/Delete payment' not in str(response_no_permission.content)
    client.logout()
    test_profile.user.user_permissions.add(permission_change_payment())
    client.login(username=test_profile.user.username, password=test_password)
    response_has_permission = client.get(url)
    assert response_has_permission.status_code == 200
    assert 'Update/Delete payment' in str(response_has_permission.content)


# Tests for PaymentListView
@pytest.mark.django_db
def test_url_and_template_for_payments_list_view(client, create_profile):
    test_password = 'test_password'
    test_profile = create_profile(password=test_password, perm=[permission_view_payment()])
    url = reverse('payment_list')
    client.login(username=test_profile.user.username, password=test_password)
    response = client.get(url)
    assert response.status_code == 200
    assert 'crm_app/payment_list.html' in [t.name for t in response.templates]


@pytest.mark.django_db
def test_no_permission_get_request_payments_list_view(client, create_profile, create_web, create_payment_to_web):
    test_password = 'test_password'
    test_profile = create_profile(password=test_password)
    url = reverse('payment_list')
    client.login(username=test_profile.user.username, password=test_password)
    response = client.get(url)
    assert response.status_code == 403


# Tests for PaymentUpdateView
@pytest.mark.django_db
def test_url_and_template_for_payments_update_view(client, create_profile, create_web, create_payment_to_web):
    test_password = 'test_password'
    test_profile = create_profile(password=test_password, perm=[permission_change_payment()])
    test_web = create_web()
    test_payment = create_payment_to_web(web=test_web, user_added=test_profile.user)
    url = reverse('payment_update', kwargs={'id': test_payment.pk})
    client.login(username=test_profile.user.username, password=test_password)
    response = client.get(url)
    assert response.status_code == 200
    assert 'crm_app/payment_update.html' in [t.name for t in response.templates]


@pytest.mark.django_db
def test_no_permission_get_request_payments_update_view(client, create_profile, create_web, create_payment_to_web):
    test_password = 'test_password'
    test_profile = create_profile(password=test_password)
    test_web = create_web()
    test_payment = create_payment_to_web(web=test_web, user_added=test_profile.user)
    url = reverse('payment_update', kwargs={'id': test_payment.pk})
    client.login(username=test_profile.user.username, password=test_password)
    response = client.get(url)
    assert response.status_code == 403


@pytest.mark.django_db
def test_successful_post_request_payments_update_view(client, create_profile, create_web, create_payment_to_web):
    test_password = 'test_password'
    test_profile = create_profile(password=test_password, perm=[permission_view_payment(), permission_change_payment()])
    original_balance = 100
    test_web = create_web(balance=original_balance)
    original_payment_sum = 0
    added_payment_sum = 50
    test_payment = create_payment_to_web(web=test_web, user_added=test_profile.user, payment_amount=original_payment_sum)
    url = reverse('payment_update', kwargs={'id': test_payment.pk})
    client.login(username=test_profile.user.username, password=test_password)
    post_data_update = {
        'payment_amount': original_payment_sum + added_payment_sum,
        'update': True
    }
    assert Web.objects.all().first().balance == original_balance
    update_response = client.post(url, data=post_data_update)
    assert update_response.status_code == 302
    assert Web.objects.all().first().balance == original_balance - added_payment_sum
    post_data_delete = {
            'payment_amount': original_payment_sum + added_payment_sum,
            'delete_payment': True
        }
    delete_response = client.post(url, data=post_data_delete)
    assert delete_response.status_code == 302
    assert Web.objects.all().first().balance == original_balance


# Tests for ProductCategoryCreationView
@pytest.mark.django_db
def test_url_and_template_for_product_category_create_view(client, create_profile):
    test_password = 'test_password'
    test_profile = create_profile(password=test_password, perm=[permission_create_product_category()])
    url = reverse('product_category_creation')
    client.login(username=test_profile.user.username, password=test_password)
    response = client.get(url)
    assert response.status_code == 200
    assert 'crm_app/product_category_creation.html' in [t.name for t in response.templates]


@pytest.mark.django_db
def test_no_permission_get_request_payments_update_view(client, create_profile):
    test_password = 'test_password'
    test_profile = create_profile(password=test_password)
    url = reverse('product_category_creation')
    client.login(username=test_profile.user.username, password=test_password)
    response = client.get(url)
    assert response.status_code == 403


@pytest.mark.django_db
def test_successful_post_request_product_category_creation(client, create_profile):
    test_password = 'test_password'
    test_user = create_profile(password=test_password,
                               perm=[permission_create_product_category()])
    client.login(username=test_user.user.username, password=test_password)
    test_category_name = 'TEST CAT'
    response = client.post(reverse('product_category_creation'), data={'category_name': test_category_name})
    assert ProductCategory.objects.all().first().category_name == test_category_name
    assert response.status_code == 302
    assert response['Location'] == reverse_lazy('product_category_detail',
                                                kwargs={'id': ProductCategory.objects.all().first().pk})


# Tests for ProductCategoryListView
@pytest.mark.django_db
def test_url_and_template_product_category_list_view(client, create_profile):
    test_password = 'test_password'
    test_profile = create_profile(password=test_password, perm=[permission_view_product_category()])
    url = reverse('product_category_list')
    client.login(username=test_profile.user.username, password=test_password)
    response = client.get(url)
    assert response.status_code == 200
    assert 'crm_app/product_category_list.html' in [t.name for t in response.templates]


@pytest.mark.django_db
def test_no_permission_get_request_product_category_list_view(client, create_profile):
    test_password = 'test_password'
    test_profile = create_profile(password=test_password)
    url = reverse('product_category_list')
    client.login(username=test_profile.user.username, password=test_password)
    response = client.get(url)
    assert response.status_code == 403


@pytest.mark.django_db
def test_add_product_category_button_permission_product_category_list(client, create_profile):
    test_password = 'test_password'
    test_profile = create_profile(password=test_password, perm=[permission_view_product_category()])
    url = reverse('product_category_list')
    client.login(username=test_profile.user.username, password=test_password)
    no_permission_response = client.get(url)
    assert no_permission_response.status_code == 200
    assert 'Add product category' not in str(no_permission_response.content)
    client.logout()
    test_profile.user.user_permissions.add(permission_create_product_category())
    client.login(username=test_profile.user.username, password=test_password)
    has_permission_response = client.get(url)
    assert has_permission_response.status_code == 200
    assert 'Add product category' in str(has_permission_response.content)


# Tests for ProductCategoryDetailView
@pytest.mark.django_db
def test_url_and_template_product_category_detail_view(client, create_profile, create_product_category):
    test_product_category = create_product_category()
    url = reverse('product_category_detail', kwargs={'id': test_product_category.pk})
    test_password = 'test_password'
    test_profile = create_profile(password=test_password, perm=[permission_view_product_category()])
    client.login(username=test_profile.user.username, password=test_password)
    response = client.get(url)
    assert response.status_code == 200
    assert 'crm_app/product_category_detail.html' in [t.name for t in response.templates]


@pytest.mark.django_db
def test_no_permission_get_request_product_category_detail_view(client, create_profile, create_product_category):
    test_product_category = create_product_category()
    url = reverse('product_category_detail', kwargs={'id': test_product_category.pk})
    test_password = 'test_password'
    test_profile = create_profile(password=test_password)
    client.login(username=test_profile.user.username, password=test_password)
    response = client.get(url)
    assert response.status_code == 403


@pytest.mark.django_db
def test_update_category_button_permission_product_category_detail_view(client, create_profile, create_product_category):
    test_product_category = create_product_category()
    url = reverse('product_category_detail', kwargs={'id': test_product_category.pk})
    test_password = 'test_password'
    test_profile = create_profile(password=test_password, perm=[permission_view_product_category()])
    client.login(username=test_profile.user.username, password=test_password)
    no_permission_response = client.get(url)
    assert no_permission_response.status_code == 200
    assert 'Update category' not in str(no_permission_response.content)
    client.logout()
    test_profile.user.user_permissions.add(permission_change_product_category())
    client.login(username=test_profile.user.username, password=test_password)
    has_permission_response = client.get(url)
    assert has_permission_response.status_code == 200
    assert 'Update category' in str(has_permission_response.content)


# Tests for ProductCategoryUpdateView
@pytest.mark.django_db
def test_url_and_template_product_category_update_view(client, create_profile, create_product_category):
    test_product_category = create_product_category()
    url = reverse('product_category_update', kwargs={'id': test_product_category.pk})
    test_password = 'test_password'
    test_profile = create_profile(password=test_password, perm=[permission_change_product_category()])
    client.login(username=test_profile.user.username, password=test_password)
    response = client.get(url)
    assert response.status_code == 200
    assert 'crm_app/product_category_update.html' in [t.name for t in response.templates]


@pytest.mark.django_db
def test_no_permission_get_request_product_category_update_view(client, create_profile, create_product_category):
    test_product_category = create_product_category()
    url = reverse('product_category_update', kwargs={'id': test_product_category.pk})
    test_password = 'test_password'
    test_profile = create_profile(password=test_password)
    client.login(username=test_profile.user.username, password=test_password)
    response = client.get(url)
    assert response.status_code == 403


@pytest.mark.dajngo_db
def test_successful_post_request_product_category_update_view(client, create_profile, create_product_category):
    original_category_name = 'test category'
    updated_category_name = 'updated name'
    test_product_category = create_product_category(category_name=original_category_name)
    url = reverse('product_category_update', kwargs={'id': test_product_category.pk})
    test_password = 'test_password'
    test_profile = create_profile(password=test_password, perm=[permission_change_product_category()])
    client.login(username=test_profile.user.username, password=test_password)
    assert ProductCategory.objects.all().first().category_name == original_category_name
    response = client.post(url, data={'category_name': updated_category_name})
    assert response.status_code == 302
    assert ProductCategory.objects.all().first().category_name == updated_category_name


# Tests for ProductCreationView
@pytest.mark.django_db
def test_url_and_template_product_creation_view(client, create_profile):
    url = reverse('product_creation')
    test_password = 'test_password'
    test_profile = create_profile(password=test_password, perm=[permission_create_product()])
    client.login(username=test_profile.user.username, password=test_password)
    response = client.get(url)
    assert response.status_code == 200
    assert 'crm_app/product_creation.html' in [t.name for t in response.templates]


@pytest.mark.dajngo_db
def test_no_permission_get_request_product_create_view(client, create_profile):
    url = reverse('product_creation')
    test_password = 'test_password'
    test_profile = create_profile(password=test_password)
    client.login(username=test_profile.user.username, password=test_password)
    response = client.get(url)
    assert response.status_code == 403


@pytest.mark.django_db
def test_successful_post_request_product_create_view(client, create_profile, create_product_category):
    test_product_category = create_product_category()
    test_password = 'test_password'
    test_profile = create_profile(password=test_password, perm=[permission_create_product()])
    url = reverse('product_creation')
    test_product_name = 'test_product'
    test_product_price = 10
    test_product_description = 'test_description'
    test_file = mock.MagicMock(spec=File)
    test_file.name = 'test_file.png'
    test_quantity_available = 5
    post_data = {
        'product_name': test_product_name,
        'product_price': test_product_price,
        'product_category': test_product_category.pk,
        'product_description': test_product_description,
        'product_image': test_file.name,
        'quantity_available': test_quantity_available
    }
    client.login(username=test_profile.user.username, password=test_password)
    response = client.post(url, data=post_data)
    assert response.status_code == 302


# Tests for ProductDetailView
@pytest.mark.django_db
def test_url_and_template_product_detail_view(client, create_profile, create_product_category, create_product):
    test_product_category = create_product_category()
    test_product = create_product(product_category=test_product_category)
    url = reverse('product_detail', kwargs={'id': test_product.pk})
    test_password = 'test_password'
    test_profile = create_profile(password=test_password, perm=[permission_view_product()])
    client.login(username=test_profile.user.username, password=test_password)
    response = client.get(url)
    assert response.status_code == 200
    assert 'crm_app/product_detail.html' in [t.name for t in response.templates]


@pytest.mark.django_db
def test_no_permission_get_request_product_detail_view(client, create_profile, create_product_category, create_product):
    test_product_category = create_product_category()
    test_product = create_product(product_category=test_product_category)
    url = reverse('product_detail', kwargs={'id': test_product.pk})
    test_password = 'test_password'
    test_profile = create_profile(password=test_password)
    client.login(username=test_profile.user.username, password=test_password)
    response = client.get(url)
    assert response.status_code == 403


@pytest.mark.django_db
def test_update_product_button_permission_product_detail_view(client, create_profile, create_product_category,
                                                              create_product):
    test_product_category = create_product_category()
    test_product = create_product(product_category=test_product_category)
    url = reverse('product_detail', kwargs={'id': test_product.pk})
    test_password = 'test_password'
    test_profile = create_profile(password=test_password, perm=[permission_view_product()])
    client.login(username=test_profile.user.username, password=test_password)
    no_permission_response = client.get(url)
    assert no_permission_response.status_code == 200
    assert 'Update product' not in str(no_permission_response.content)
    client.logout()
    test_profile.user.user_permissions.add(permission_change_product())
    client.login(username=test_profile.user.username, password=test_password)
    has_permission_response = client.get(url)
    assert has_permission_response.status_code == 200
    assert 'Update product' in str(has_permission_response.content)


# Tests for ProductListView
@pytest.mark.django_db
def test_url_and_template_product_list_view(client, create_profile):
    url = reverse('product_list')
    test_password = 'test_password'
    test_profile = create_profile(password=test_password, perm=[permission_view_product()])
    client.login(username=test_profile.user.username, password=test_password)
    response = client.get(url)
    assert response.status_code == 200
    assert 'crm_app/product_list.html' in [t.name for t in response.templates]


@pytest.mark.django_db
def test_no_permission_get_request_product_list_view(client, create_profile):
    url = reverse('product_list')
    test_password = 'test_password'
    test_profile = create_profile(password=test_password)
    client.login(username=test_profile.user.username, password=test_password)
    response = client.get(url)
    assert response.status_code == 403


@pytest.mark.django_db
def test_update_product_button_permission_product_list_view(client, create_profile):
    url = reverse('product_list')
    test_password = 'test_password'
    test_profile = create_profile(password=test_password, perm=[permission_view_product()])
    client.login(username=test_profile.user.username, password=test_password)
    no_permission_response = client.get(url)
    assert no_permission_response.status_code == 200
    assert 'Add new product' not in str(no_permission_response.content)
    client.logout()
    test_profile.user.user_permissions.add(permission_create_product())
    client.login(username=test_profile.user.username, password=test_password)
    has_permission_response = client.get(url)
    assert has_permission_response.status_code == 200
    assert 'Add new product' in str(has_permission_response.content)


# Tests for ProductUpdateView
@pytest.mark.django_db
def test_url_and_template_product_update_view(client, create_profile, create_product_category, create_product):
    test_product_category = create_product_category()
    test_product = create_product(product_category=test_product_category)
    url = reverse('product_update', kwargs={'id': test_product.pk})
    test_password = 'test_password'
    test_profile = create_profile(password=test_password, perm=[permission_change_product()])
    client.login(username=test_profile.user.username, password=test_password)
    response = client.get(url)
    assert response.status_code == 200
    assert 'crm_app/product_update.html' in [t.name for t in response.templates]


@pytest.mark.django_db
def test_no_permission_get_request_product_update_view(client, create_profile, create_product_category, create_product):
    test_product_category = create_product_category()
    test_product = create_product(product_category=test_product_category)
    url = reverse('product_update', kwargs={'id': test_product.pk})
    test_password = 'test_password'
    test_profile = create_profile(password=test_password)
    client.login(username=test_profile.user.username, password=test_password)
    response = client.get(url)
    assert response.status_code == 403


@pytest.mark.django_db
def test_successful_post_request_product_update_view(client, create_profile, create_product_category, create_product):
    test_product_category = create_product_category()
    original_product_name = 'test_product_name'
    updated_product_name = 'updated_product_name'
    test_product = create_product(product_category=test_product_category, product_name=original_product_name)
    url = reverse('product_update', kwargs={'id': test_product.pk})
    test_password = 'test_password'
    test_profile = create_profile(password=test_password, perm=[permission_change_product()])
    post_data = {
        'product_name': updated_product_name,
        'product_price': test_product.product_price,
        'product_category': test_product.product_category.pk,
        'product_description': test_product.product_description,
        # 'id_product_image': test_product.product_image,
        'quantity_available': test_product.quantity_available
    }
    client.login(username=test_profile.user.username, password=test_password)
    assert Product.objects.all().first().product_name == original_product_name
    response = client.post(url, data=post_data)
    assert response.status_code == 302
    assert Product.objects.all().first().product_name == updated_product_name


# Tests for OfferCreationView
@pytest.mark.django_db
def test_url_and_template_offer_creation_view(client, create_profile):
    url = reverse('offer_creation')
    test_password = 'test_password'
    test_profile = create_profile(password=test_password, perm=[permission_create_offer()])
    client.login(username=test_profile.user.username, password=test_password)
    response = client.get(url)
    assert response.status_code == 200
    assert 'crm_app/offer_creation.html' in [t.name for t in response.templates]


@pytest.mark.dajngo_db
def test_no_permission_get_request_offer_create_view(client, create_profile):
    url = reverse('offer_creation')
    test_password = 'test_password'
    test_profile = create_profile(password=test_password)
    client.login(username=test_profile.user.username, password=test_password)
    response = client.get(url)
    assert response.status_code == 403


@pytest.mark.django_db
def test_successful_post_request_offer_create_view(client, create_profile, create_product_category, create_product,
                                                   create_web):
    test_product_category = create_product_category()
    test_product = create_product(product_category=test_product_category)
    test_web = create_web()
    test_password = 'test_password'
    test_profile = create_profile(password=test_password, perm=[permission_create_offer()])
    url = reverse('offer_creation')
    test_cost_of_a_click = 10.0
    post_data = {
        'web': test_web.pk,
        'product': test_product.pk,
        'click_cost': test_cost_of_a_click,
        'website_url': ''
    }
    client.login(username=test_profile.user.username, password=test_password)
    response = client.post(url, data=post_data)
    assert response.status_code == 302
    assert str(Offer.objects.all().first()) == f'{test_web.web_name}: {test_product.product_name}'


# Tests for OfferDetailView
@pytest.mark.django_db
def test_url_and_template_offer_detail_view(client, create_profile, create_product_category, create_product,
                                            create_web, create_offer):
    test_product_category = create_product_category()
    test_product = create_product(product_category=test_product_category)
    test_web = create_web()
    test_offer = create_offer(product=test_product, web=test_web)
    url = reverse('offer_detail', kwargs={'id': test_offer.pk})
    test_password = 'test_password'
    test_profile = create_profile(password=test_password, perm=[permission_view_offer()])
    client.login(username=test_profile.user.username, password=test_password)
    response = client.get(url)
    assert response.status_code == 200
    assert 'crm_app/offer_detail.html' in [t.name for t in response.templates]


@pytest.mark.django_db
def test_no_permission_get_request_offer_detail_view(client, create_profile, create_product_category, create_product,
                                                     create_web, create_offer):
    test_product_category = create_product_category()
    test_product = create_product(product_category=test_product_category)
    test_web = create_web()
    test_offer = create_offer(product=test_product, web=test_web)
    url = reverse('offer_detail', kwargs={'id': test_offer.pk})
    test_password = 'test_password'
    test_profile = create_profile(password=test_password)
    client.login(username=test_profile.user.username, password=test_password)
    response = client.get(url)
    assert response.status_code == 403


@pytest.mark.django_db
def test_update_product_button_permission_offer_detail_view(client, create_profile, create_product_category,
                                                            create_product, create_web, create_offer):
    test_product_category = create_product_category()
    test_product = create_product(product_category=test_product_category)
    test_web = create_web()
    test_offer = create_offer(product=test_product, web=test_web)
    url = reverse('offer_detail', kwargs={'id': test_offer.pk})
    test_password = 'test_password'
    test_profile = create_profile(password=test_password, perm=[permission_view_offer()])
    client.login(username=test_profile.user.username, password=test_password)
    no_permission_response = client.get(url)
    assert no_permission_response.status_code == 200
    assert 'Update offer' not in str(no_permission_response.content)
    client.logout()
    test_profile.user.user_permissions.add(permission_change_offer())
    client.login(username=test_profile.user.username, password=test_password)
    has_permission_response = client.get(url)
    assert has_permission_response.status_code == 200
    assert 'Update offer' in str(has_permission_response.content)


# Tests for OfferListView
@pytest.mark.django_db
def test_url_and_template_offer_list_view(client, create_profile):
    url = reverse('offer_list')
    test_password = 'test_password'
    test_profile = create_profile(password=test_password, perm=[permission_view_offer()])
    client.login(username=test_profile.user.username, password=test_password)
    response = client.get(url)
    assert response.status_code == 200
    assert 'crm_app/offer_list.html' in [t.name for t in response.templates]


@pytest.mark.django_db
def test_no_permission_get_request_offer_list_view(client, create_profile):
    url = reverse('offer_list')
    test_password = 'test_password'
    test_profile = create_profile(password=test_password)
    client.login(username=test_profile.user.username, password=test_password)
    response = client.get(url)
    assert response.status_code == 403


@pytest.mark.django_db
def test_update_product_button_permission_offer_list_view(client, create_profile):
    url = reverse('offer_list')
    test_password = 'test_password'
    test_profile = create_profile(password=test_password, perm=[permission_view_offer()])
    client.login(username=test_profile.user.username, password=test_password)
    no_permission_response = client.get(url)
    assert no_permission_response.status_code == 200
    assert 'Add offer' not in str(no_permission_response.content)
    client.logout()
    test_profile.user.user_permissions.add(permission_create_offer())
    client.login(username=test_profile.user.username, password=test_password)
    has_permission_response = client.get(url)
    assert has_permission_response.status_code == 200
    assert 'Add offer' in str(has_permission_response.content)


# Tests for OfferUpdateView
@pytest.mark.django_db
def test_url_and_template_offer_update_view(client, create_profile, create_product_category, create_product, create_web,
                                            create_offer):
    test_product_category = create_product_category()
    test_product = create_product(product_category=test_product_category)
    test_web = create_web()
    test_offer = create_offer(product=test_product, web=test_web)
    url = reverse('offer_update', kwargs={'id': test_offer.pk})
    test_password = 'test_password'
    test_profile = create_profile(password=test_password, perm=[permission_change_offer()])
    client.login(username=test_profile.user.username, password=test_password)
    response = client.get(url)
    assert response.status_code == 200
    assert 'crm_app/offer_update.html' in [t.name for t in response.templates]


@pytest.mark.django_db
def test_no_permission_get_request_offer_update_view(client, create_profile, create_product_category, create_product,
                                                     create_web, create_offer):
    test_product_category = create_product_category()
    test_product = create_product(product_category=test_product_category)
    test_web = create_web()
    test_offer = create_offer(product=test_product, web=test_web)
    url = reverse('offer_update', kwargs={'id': test_offer.pk})
    test_password = 'test_password'
    test_profile = create_profile(password=test_password)
    client.login(username=test_profile.user.username, password=test_password)
    response = client.get(url)
    assert response.status_code == 403


@pytest.mark.django_db
def test_successful_post_request_offer_update_view(client, create_profile, create_product_category, create_product,
                                                   create_web, create_offer):
    test_product_category = create_product_category()
    test_product = create_product(product_category=test_product_category)
    test_web = create_web()
    original_click_cost = 40
    updated_click_cost = 45
    test_offer = create_offer(product=test_product, web=test_web, click_cost=original_click_cost)
    url = reverse('offer_update', kwargs={'id': test_offer.pk})
    test_password = 'test_password'
    test_profile = create_profile(password=test_password, perm=[permission_change_offer()])
    post_data = {
        'click_cost': updated_click_cost
    }
    client.login(username=test_profile.user.username, password=test_password)
    assert Offer.objects.all().first().click_cost == original_click_cost
    response = client.post(url, data=post_data)
    assert response.status_code == 302
    assert Offer.objects.all().first().click_cost == updated_click_cost


# Tests for ProfileDetailView
@pytest.mark.django_db
def test_url_and_template_profile_detail_view(client, create_profile):
    test_password = 'test_password'
    test_profile = create_profile(password=test_password, perm=[permission_view_profile()])
    url = reverse('profile_detail', kwargs={'id': test_profile.pk})
    client.login(username=test_profile.user.username, password=test_password)
    response = client.get(url)
    assert response.status_code == 200
    assert 'crm_app/profile_detail.html' in [t.name for t in response.templates]


@pytest.mark.django_db
def test_no_permission_get_request_profile_detail_view(client, create_profile):
    test_password = 'test_password'
    test_profile = create_profile(password=test_password)
    url = reverse('profile_detail', kwargs={'id': test_profile.pk})
    client.login(username=test_profile.user.username, password=test_password)
    response = client.get(url)
    assert response.status_code == 403


# Tests for ProfileListView
@pytest.mark.django_db
def test_url_and_template_profile_list_view(client, create_profile):
    url = reverse('profile_list')
    test_password = 'test_password'
    test_profile = create_profile(password=test_password, perm=[permission_view_profile()])
    client.login(username=test_profile.user.username, password=test_password)
    response = client.get(url)
    assert response.status_code == 200
    assert 'crm_app/profile_list.html' in [t.name for t in response.templates]


@pytest.mark.django_db
def test_no_permission_get_request_profile_list_view(client, create_profile):
    url = reverse('profile_list')
    test_password = 'test_password'
    test_profile = create_profile(password=test_password)
    client.login(username=test_profile.user.username, password=test_password)
    response = client.get(url)
    assert response.status_code == 403
