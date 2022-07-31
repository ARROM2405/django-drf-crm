from django.http import JsonResponse
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

from .serializers import *
from crm_app.models import Lead, Web, Offer

# 23j4hhk23kl234234!!24sd 1008
# kdladkfgjhlsdfhglk1111


class LeadListApiView(ListAPIView):
    serializer_class = LeadSerializer

    def get_queryset(self):
        web = Web.objects.filter(web_api_key=self.kwargs.get('web_api_key')).first()
        offers = Offer.objects.filter(web=web)
        leads = Lead.objects.filter(offer_FK__in=offers)
        return leads


class LeadCreateApiView(CreateAPIView):
    serializer_class = LeadSerializer

    def post(self, request, *args, **kwargs):
        web_api_key = self.kwargs.get('web_api_key')
        if Web.objects.filter(web_api_key=web_api_key):
            return super().post(request, *args, **kwargs)
        else:
            return Response(data={'response': 'incorrect api key'})


class ProductListApiView(ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        web = Web.objects.filter(web_api_key=self.kwargs.get('web_api_key')).first()
        if web:
            return Product.objects.all()
        return Product.objects.none()


class OfferListApiView(ListAPIView):
    serializer_class = OfferSerializer

    def get_queryset(self, *args, **kwargs):
        web = Web.objects.filter(web_api_key=self.kwargs.get('web_api_key')).first()
        if web:
            return Offer.objects.filter(web=web)
        return Offer.objects.none()
