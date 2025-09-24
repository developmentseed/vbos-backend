from django_filters import (
    FilterSet,
    CharFilter,
    OrderingFilter,
    DateFromToRangeFilter,
    ModelChoiceFilter,
)

from .models import (
    RasterDataset,
    TabularItem,
    VectorDataset,
    TabularDataset,
    Cluster,
    VectorItem,
)


class DatasetFilter(FilterSet):
    name = CharFilter(field_name="name", lookup_expr="icontains")
    source = CharFilter(field_name="source", lookup_expr="icontains")
    type = CharFilter(field_name="type", lookup_expr="iexact")
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


class TabularItemFilter(FilterSet):
    filter = CharFilter(
        field_name="data",
        method="filter_metadata",
        help_text="""Filter by the content of the data JSONField.""",
    )

    def split_values(self, value):
        return [
            [i.strip() for i in t.split("=")]  # remove leading and ending spaces
            for t in value.split(",")
            if len(t.split("=")) == 2
        ]

    def filter_metadata(self, queryset, name, value):
        queries = self.split_values(value)

        if not queries:
            return queryset

        for key, val in queries:
            # For exact matching (current behavior)
            try:
                # Try numeric types
                if "." in val:
                    filter_value = float(val)
                else:
                    filter_value = int(val)
            except ValueError:
                # Handle booleans
                if val.lower() in ["true", "false"]:
                    filter_value = val.lower() == "true"
                else:
                    filter_value = val

            # Use exact lookup
            lookup = f"{name}__{key}"
            queryset = queryset.filter(**{lookup: filter_value})

        return queryset

    class Meta:
        model = TabularItem
        fields = ["filter", "id"]


class VectorItemFilter(TabularItemFilter):
    filter = CharFilter(
        field_name="metadata",
        method="filter_metadata",
        help_text="""Filter by the content of the metadata JSONField.""",
    )

    class Meta:
        model = VectorItem
        fields = ["filter", "id"]
