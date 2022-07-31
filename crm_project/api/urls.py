from django.urls import path
from .views import *

urlpatterns = [
    path('<str:web_api_key>/lead_list/', LeadListApiView.as_view(), name='lead_list_api'),
    path('<str:web_api_key>/lead_creation/', LeadCreateApiView.as_view(), name='lead_creation_api'),
    path('<str:web_api_key>/product_list/', ProductListApiView.as_view(), name='product_list_api'),
    path('<str:web_api_key>/offer_list/', OfferListApiView.as_view(), name='offer_list_api'),
]