import json

import pytest
from django.urls import reverse
from fixtures import *


@pytest.mark.django_db
def test_lead_list_api_view(client, create_web, create_product_category, create_product, create_offer,
                                          create_lead):
    leads_count = 5
    web_api_key_correct = 'abc'
    web_api_key_incorrect = '123'
    test_web = create_web(web_api_key=web_api_key_correct)
    test_product_category = create_product_category()
    test_product = create_product(product_category=test_product_category)
    test_offer = create_offer(web=test_web, product=test_product)
    for lead in range(leads_count):
        create_lead(offer=test_offer)
    incorrect_api_key_response = client.get(reverse('lead_list_api', kwargs={'web_api_key': web_api_key_incorrect}))
    assert incorrect_api_key_response.status_code == 200
    assert incorrect_api_key_response.json().get('count') == 0
    correct_api_key_response = client.get(reverse('lead_list_api', kwargs={'web_api_key': web_api_key_correct}))
    assert correct_api_key_response.status_code == 200
    assert correct_api_key_response.json().get('count') == leads_count


@pytest.mark.django_db
def test_lead_create_view(client, create_web, create_product_category, create_product, create_offer):
    web_api_key_correct = 'abc'
    web_api_key_incorrect = '123'
    test_web = create_web(web_api_key=web_api_key_correct)
    test_product_category = create_product_category()
    test_product = create_product(product_category=test_product_category)
    test_offer = create_offer(web=test_web, product=test_product)
    post_data = {
        'offer_FK': test_offer.pk,
        'customer_first_name': 'test_first_name',
        'customer_last_name': 'test_last_name',
        'contact_phone': '123-123-123'
    }
    incorrect_api_key_response = client.post(reverse('lead_creation_api',
                                                     kwargs={'web_api_key': web_api_key_incorrect}), data=post_data)
    assert incorrect_api_key_response.status_code == 200
    assert incorrect_api_key_response.json().get('response') == 'incorrect api key'
    correct_api_key_response = client.post(reverse('lead_creation_api',
                                                   kwargs={'web_api_key': web_api_key_correct}), data=post_data)
    assert correct_api_key_response.status_code == 201


@pytest.mark.django_db
def test_product_list_view(client, create_web, create_product_category, create_product):
    products_count = 5
    web_api_key_correct = 'abc'
    web_api_key_incorrect = '123'
    test_web = create_web(web_api_key=web_api_key_correct)
    test_product_category = create_product_category()
    for product in range(products_count):
        create_product(product_name=f'{product}', product_category=test_product_category)
    incorrect_api_key_response = client.get(reverse('product_list_api', kwargs={'web_api_key': web_api_key_incorrect}))
    assert incorrect_api_key_response.status_code == 200
    assert incorrect_api_key_response.json().get('count') == 0
    correct_api_key_response = client.get(reverse('product_list_api', kwargs={'web_api_key': web_api_key_correct}))
    assert correct_api_key_response.status_code == 200
    assert correct_api_key_response.json().get('count') == products_count


@pytest.mark.django_db
def test_offer_list_view(client, create_web, create_product_category, create_product, create_offer):
    offers_count = 5
    web_api_key_correct = 'abc'
    web_api_key_incorrect = '123'
    test_web = create_web(web_api_key=web_api_key_correct)
    test_product_category = create_product_category()
    test_product = create_product(product_category=test_product_category)
    for product in range(offers_count):
        create_offer(product=test_product, web=test_web)
    incorrect_api_key_response = client.get(reverse('offer_list_api', kwargs={'web_api_key': web_api_key_incorrect}))
    assert incorrect_api_key_response.status_code == 200
    assert incorrect_api_key_response.json().get('count') == 0
    correct_api_key_response = client.get(reverse('offer_list_api', kwargs={'web_api_key': web_api_key_correct}))
    assert correct_api_key_response.status_code == 200
    assert correct_api_key_response.json().get('count') == offers_count
