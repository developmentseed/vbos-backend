from django_filters import (
    FilterSet,
    BooleanFilter,
    CharFilter,
    OrderingFilter,
    DateFromToRangeFilter,
    ModelChoiceFilter,
)

from .models import RasterDataset, VectorDataset, TabularDataset


class DatasetFilter(FilterSet):
    name = CharFilter(field_name="name", lookup_expr="icontains")
    created = DateFromToRangeFilter()
    updated = DateFromToRangeFilter()
    order_by = OrderingFilter(
        fields=("name", "id", "updated", "created"),
    )


class RasterDatasetFilter(DatasetFilter):
    class Meta:
        model = RasterDataset
        fields = ["name", "created", "updated"]


class VectorDatasetFilter(DatasetFilter):
    class Meta:
        model = VectorDataset
        fields = ["name", "created", "updated"]


class TabularDatasetFilter(DatasetFilter):
    class Meta:
        model = TabularDataset
        fields = ["name", "created", "updated"]
