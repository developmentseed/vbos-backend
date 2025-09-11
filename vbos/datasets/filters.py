from django_filters import (
    FilterSet,
    BooleanFilter,
    CharFilter,
    OrderingFilter,
    DateFromToRangeFilter,
    ModelChoiceFilter,
)

from .models import RasterDataset, VectorDataset, TabularDataset, Cluster


class DatasetFilter(FilterSet):
    name = CharFilter(field_name="name", lookup_expr="icontains")
    source = CharFilter(field_name="source", lookup_expr="icontains")
    cluster = ModelChoiceFilter(
        field_name="cluster__name",
        to_field_name="name__iexact",
        queryset=Cluster.objects.all(),
    )
    created = DateFromToRangeFilter()
    updated = DateFromToRangeFilter()
    order_by = OrderingFilter(
        fields=("name", "id", "updated", "created"),
    )


class RasterDatasetFilter(DatasetFilter):
    class Meta:
        model = RasterDataset
        fields = ["name", "source", "cluster", "created", "updated"]


class VectorDatasetFilter(DatasetFilter):
    class Meta:
        model = VectorDataset
        fields = ["name", "source", "cluster", "created", "updated"]


class TabularDatasetFilter(DatasetFilter):
    class Meta:
        model = TabularDataset
        fields = ["name", "source", "cluster", "created", "updated"]
