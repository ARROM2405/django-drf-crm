from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import *

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('home_page/<str:stat>/', HomePageView.as_view(), name='home_page'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('web_creation/', WebCreationView.as_view(), name='web_creation'),
    path('web_detail/<int:id>/', WebDetailView.as_view(), name='web_detail'),
    path('web_list/', WebListView.as_view(), name='web_list'),
    path('web_update/<int:id>/', WebUpdateView.as_view(), name='web_update'),
    path('lead_creation/', LeadCreationView.as_view(), name='lead_creation'),
    path('lead_detail/<int:id>/', LeadDetailView.as_view(), name='lead_detail'),
    path('lead_list/', LeadListView.as_view(), name='lead_list'),
    path('product_category_creation/', ProductCategoryCreationView.as_view(), name='product_category_creation'),
    path('product_category_detail/<int:id>/', ProductCategoryDetailView.as_view(), name='product_category_detail'),
    path('product_category_list/', ProductCategoryListView.as_view(), name='product_category_list'),
    path('product_category_update/<int:id>/', ProductCategoryUpdateView.as_view(), name='product_category_update'),
    path('product_creation/', ProductCreationView.as_view(), name='product_creation'),
    path('product_detail/<int:id>/', ProductDetailView.as_view(), name='product_detail'),
    path('product_list/', ProductListView.as_view(), name='product_list'),
    path('product_update/<int:id>/', ProductUpdateView.as_view(), name='product_update'),
    path('offer_creation/', OfferCreationView.as_view(), name='offer_creation'),
    path('offer_detail/<int:id>/', OfferDetailView.as_view(), name='offer_detail'),
    path('offer_list/', OfferListView.as_view(), name='offer_list'),
    path('offer_update/<int:id>/', OfferUpdateView.as_view(), name='offer_update'),
    path('order_creation/', OrderCreationView.as_view(), name='order_creation'),
    path('order_detail/<int:id>/', OrderDetailView.as_view(), name='order_detail'),
    path('order_list/', OrderListView.as_view(), name='order_list'),
    path('order_update/<int:id>/', OrderUpdateView.as_view(), name='order_update'),
    path('payment_creation/<int:web_id>/', PaymentCreationView.as_view(), name='payment_creation'),
    path('payment_detail/<int:id>/', PaymentDetailView.as_view(), name='payment_detail'),
    path('payment_list/', PaymentListView.as_view(), name='payment_list'),
    path('payment_update/<int:id>/', PaymentUpdateView.as_view(), name='payment_update'),
    path('profile_detail/<int:id>/', ProfileDetailView.as_view(), name='profile_detail'),
    path('profile_list/', ProfileListView.as_view(), name='profile_list')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
