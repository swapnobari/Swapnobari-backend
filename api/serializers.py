from rest_framework import serializers
 
 
class ReorderSerializer(serializers.Serializer):
    """Body for every `/reorder/` endpoint: ids in the order they should appear."""
 
    ids = serializers.ListField(child=serializers.IntegerField(min_value=1), allow_empty=False)
 
    def validate_ids(self, value):
        if len(value) != len(set(value)):
            raise serializers.ValidationError("Duplicate ids are not allowed.")
        return value


def make_slug_field(queryset):
    """Optional, unicode-friendly, unique slug field. Leave it blank to auto-generate."""
    from rest_framework.validators import UniqueValidator
 
    return serializers.SlugField(
        required=False,
        allow_blank=True,
        allow_unicode=True,
        max_length=200,
        validators=[UniqueValidator(queryset=queryset)],
    )