from django.db.models import Max
from rest_framework import serializers
 
from team.models import TeamMember
 
 
class TeamMemberSerializer(serializers.ModelSerializer):
    
    photo = serializers.ImageField(
        required=False,
        allow_null=True,
    )
    
    class Meta:
        model = TeamMember
        fields = [
            "id",
            "name",
            "designation",
            "bio",
            "photo",
            "email",
            "phone",
            "facebook_url",
            "linkedin_url",
            "order",
            "is_active",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]
 
    def create(self, validated_data):
        # new member goes to the end unless an order is given
        if "order" not in validated_data:
            highest = TeamMember.objects.aggregate(m=Max("order"))["m"]
            validated_data["order"] = 0 if highest is None else highest + 1
        return super().create(validated_data)