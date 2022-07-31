from rest_framework import serializers
from crm_app.models import Lead, Offer, Product, ProductCategory


class LeadSerializer(serializers.ModelSerializer):
    lead_id = serializers.IntegerField(read_only=True)
    status = serializers.CharField(read_only=True)
    lead_cost = serializers.DecimalField(max_digits=10, decimal_places=2, min_value=0, read_only=True)

    class Meta:
        model = Lead
        fields = ['lead_id', 'status', 'created_at', 'offer_FK', 'customer_first_name', 'customer_last_name',
                  'contact_phone', 'lead_cost']

    def create(self, validated_data):
        validated_data['lead_cost'] = Offer.objects.get(pk=validated_data.get('offer_FK').pk).click_cost
        return super().create(validated_data)


class ProductSerializer(serializers.ModelSerializer):

    def get_category_name(self, obj):
        return ProductCategory.objects.get(pk=obj.product_category.pk).category_name

    product_category_name = serializers.SerializerMethodField(method_name='get_category_name')

    class Meta:
        model = Product
        fields = ['product_id', 'product_name', 'product_category_name', 'product_description']


class OfferSerializer(serializers.ModelSerializer):
    def get_product_name(self, obj):
        return obj.product.product_name

    product_name = serializers.SerializerMethodField(method_name='get_product_name')

    class Meta:
        model = Offer
        fields = ['product_name', 'click_cost', 'website_url']