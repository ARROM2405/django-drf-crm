from django.urls import path
from .views import *

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('home_page/', HomePageView.as_view(), name='home_page'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('web_creation/', WebCreationView.as_view(), name='web_creation'),
    path('web_detail/<int:id>/', WebDetailView.as_view(), name='web_detail'),
    path('web_list/', WebListView.as_view(), name='web_list'),
    path('lead_creation/', LeadCreationView.as_view(), name='lead_creation'),
    path('lead_detail/<int:id>/', LeadDetailView.as_view(), name='lead_detail'),
    path('product_category_creation/', ProductCategoryCreationView.as_view(), name='product_category_creation'),
    path('product_category_detail/<int:id>/', ProductCategoryDetailView.as_view(), name='product_category_detail'),
    path('product_category_list/', ProductCategoryListView.as_view(), name='product_category_list'),
    path('product_creation/', ProductCreationView.as_view(), name='product_creation'),
    path('product_detail/<int:id>/', ProductDetailView.as_view(), name='product_detail'),
    path('product_list/', ProductListView.as_view(), name='product_list'),
]
