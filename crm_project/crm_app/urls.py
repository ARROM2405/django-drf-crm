from django.urls import path
from .views import *

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('home_page/', HomePageView.as_view(), name='home_page'),
    path('login/', UserLoginView.as_view(), name='login')
]
