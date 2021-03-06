from crm_app.forms import *
from fixtures import *


@pytest.mark.django_db
def test_registration_form_fields_list():
    form = RegistrationForm()
    assert list(form.fields.keys()) == ['username', 'password1', 'password2']


@pytest.mark.django_db
def test_web_creation_form_fields():
    form = WebCreationForm()
    assert list(form.fields.keys()) == ['web_name', 'web_description', 'web_api_key', 'balance']


@pytest.mark.django_db
def test_lead_creation_form_fields():
    form = LeadCreationForm()
    assert list(form.fields.keys()) == ['offer_FK', 'contact_phone', 'customer_first_name', 'customer_last_name']


@pytest.mark.django_db
def test_lead_creation_form_help_text():
    form = LeadCreationForm()
    assert form.fields.get('contact_phone').widget.attrs.get('placeholder') == '123-123-123'


@pytest.mark.django_db
def test_lead_creation_form_form_is_valid_method(create_web, create_product_category, create_product, create_offer):
    test_web = create_web()
    test_product_category = create_product_category()
    test_product = create_product(product_category=test_product_category)
    test_offer = create_offer(product=test_product, web=test_web)
    form = LeadCreationForm(
        data={
            'offer_FK': test_offer.pk,
            'contact_phone': '111-111-111',
            'customer_first_name': 'test_fn',
            'customer_last_name': 'test_ln'
        }
    )
    assert form.is_valid()


@pytest.mark.django_db
def test_product_category_creation_form_fields():
    form = ProductCategoryCreationForm()
    assert list(form.fields.keys()) == ['category_name']


@pytest.mark.django_db
def test_product_creation_form_fields():
    form = ProductCreationForm()
    assert list(form.fields.keys()) == ['product_name', 'product_price', 'product_category', 'product_description',
                                        'product_image', 'quantity_available']


@pytest.mark.django_db
def test_product_creation_form_label():
    form = ProductCreationForm()
    assert form['product_category'].label == 'Product category'


@pytest.mark.django_db
def test_offer_creation_form_fields():
    form = OfferCreationForm()
    assert list(form.fields.keys()) == ['web', 'product', 'click_cost', 'website_url']


@pytest.mark.django_db
def test_payment_creation_form_fields():
    form = PaymentCreationForm()
    assert list(form.fields.keys()) == ['web_FK', 'payment_amount']


@pytest.mark.django_db
def test_order_creation_form_fields():
    form = OrderCreationForm()
    assert list(form.fields.keys()) == ['customer_first_name', 'customer_last_name', 'status', 'sent_date',
                                        'contact_phone', 'delivery_city', 'delivery_street', 'delivery_house_number',
                                        'delivery_apartment_number', 'delivery_zip_code', 'product_1',
                                        'product_1_quantity', 'product_1_price', 'product_2', 'product_2_quantity',
                                        'product_2_price', 'product_3', 'product_3_quantity', 'product_3_price']
