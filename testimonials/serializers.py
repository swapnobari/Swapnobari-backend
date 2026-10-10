from django.db.models import Max
from rest_framework import serializers
 
from testimonials.models import Testimonial
 
 
class TestimonialSerializer(serializers.ModelSerializer):
    
    photo = serializers.ImageField(
        required=False,
        allow_null=True,
    )
    
    class Meta:
        model = Testimonial
        fields = [
            "id",
            "name",
            "designation",
            "photo",
            "rating",
            "message",
            "order",
            "is_active",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]
 
    def create(self, validated_data):
        # new testimonial goes to the end unless an order is given
        if "order" not in validated_data:
            highest = Testimonial.objects.aggregate(m=Max("order"))["m"]
            validated_data["order"] = 0 if highest is None else highest + 1
        return super().create(validated_data)