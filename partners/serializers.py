from django.db.models import Max
from rest_framework import serializers
 
from partners.models import Partner
 
 
class PartnerSerializer(serializers.ModelSerializer):
    
    logo = serializers.ImageField(
        required=False,
        allow_null=True,
    )
    
    class Meta:
        model = Partner
        fields = [
            "id",
            "name",
            "logo",
            "website_url",
            "order",
            "is_active",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]
 
    def create(self, validated_data):
        # new partner goes to the end unless an order is given
        if "order" not in validated_data:
            highest = Partner.objects.aggregate(m=Max("order"))["m"]
            validated_data["order"] = 0 if highest is None else highest + 1
        return super().create(validated_data)
 