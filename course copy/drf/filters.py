from django_filters import rest_framework as filters
from .models import Cat


class CatFilter(filters.FilterSet):
    min_weight = filters.NumberFilter(field_name="weight", lookup_expr="gte")
    max_weight = filters.NumberFilter(field_name="weight", lookup_expr="lte")
    breed_name = filters.CharFilter(
        field_name="breed__name", lookup_expr="icontains"
    )

    class Meta:
        model = Cat
        fields = [
            "nickname",
            "breed",
            "min_weight",
            "max_weight",
            "breed_name",
            "created_at",
        ]
