import pprint
from unittest import TestCase

import pytest
from django.contrib import auth
from django.shortcuts import reverse
from crm_app.tests.fixtures import *
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse_lazy


# Permissions
def permission_create_lead():
    ct = ContentType.objects.get(app_label='crm_app', model='lead')
    perm = Permission.objects.create(codename='create_lead', name='can add lead', content_type=ct)
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
    test_user = create_profile(password=test_password, perm=permission_create_lead())
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
    test_profile = create_profile(password=test_password, perm=permission_create_lead())
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
                                              'id_contact_phone:': contact_phone,
                                              'customer_first_n˜ame': customer_fn,
                                              'customer_last_name': customer_ln},
                           )
    pprint.pprint(response.content)
    assert response.status_code == 302
    assert response['Location'] == redirect_url
    assert Lead.objects.all().first().lead_cost == test_offer.lead_cost


# Tests for LeadDetailView
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


def test_unauthorised_user_get_request_lead_detail(client, create_profile, create_product_category, create_product,
                                                   create_web, create_offer, create_lead):
    # test_password = 'test_password'
    # test_profile = create_profile(password=test_password, perm=permission_view_lead())
    test_product_category = create_product_category()
    test_product = create_product(product_category=test_product_category)
    test_web = create_web()
    test_offer = create_offer(product=test_product, web=test_web)
    test_lead = create_lead(offer=test_offer)
    # client.login(username=test_profile.user.username, password=test_password)
    response = client.get(reverse('lead_detail', kwargs={'id': test_lead.pk}))
    assert response.status_code == 302
    assert reverse('login') in response['Location']


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


def test_has_permission_get_request_lead_detail(client, create_profile, create_product_category, create_product,
                                               create_web, create_offer, create_lead):
    test_password = 'test_password'
    test_profile = create_profile(password=test_password, perm=permission_view_lead())
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


# Tests for LeadListView
def test_template_used_lead_list_view(client, create_profile):
    test_password = 'test_password'
    test_profile = create_profile(password=test_password, perm=permission_view_lead())
    url = reverse('lead_list')
    client.login(username=test_profile.user.username, password=test_password)
    response = client.get(url)
    assert 'crm_app/lead_list.html' in (t.name for t in response.templates)


# Tests for ProductCategoryCreationLead
@pytest.mark.django_db
def test_product_category_creation(client, create_profile):
    test_password = 'test_password'
    test_user = create_profile(password=test_password,
                               perm=permission_create_product_category())
    client.login(username=test_user.user.username, password=test_password)
    test_category_name = 'TEST CAT'
    response = client.post(reverse('product_category_creation'), data={'category_name': test_category_name})
    pprint.pprint(response.content)
    assert len(ProductCategory.objects.all()) == 1
    assert ProductCategory.objects.all().first().category_name == test_category_name
    assert response.status_code == 302
    assert response['Location'] == reverse_lazy('product_category_detail',
                                                kwargs={'id': ProductCategory.objects.all().first().pk})


