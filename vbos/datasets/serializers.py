from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer

from .models import (
    Cluster,
    RasterDataset,
    TabularDataset,
    TabularItem,
    VectorDataset,
    VectorItem,
)


class ClusterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cluster
        fields = ["id", "name"]


class RasterDatasetSerializer(serializers.ModelSerializer):
    file = serializers.ReadOnlyField(source="file.file.url")
    cluster = serializers.ReadOnlyField(source="cluster.name")

    class Meta:
        model = RasterDataset
        fields = [
            "id",
            "name",
            "created",
            "updated",
            "cluster",
            "type",
            "source",
            "file",
        ]


class VectorDatasetSerializer(serializers.ModelSerializer):
    cluster = serializers.ReadOnlyField(source="cluster.name")

    class Meta:
        model = VectorDataset
        fields = ["id", "name", "created", "updated", "cluster", "type", "source"]


class VectorItemSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = VectorItem
        geo_field = "geometry"
        fields = ["id", "metadata"]

    def get_properties(self, instance, fields):
        # This is a PostgreSQL HStore field, which django maps to a dict
        return instance.metadata

    def unformat_geojson(self, feature):
        attrs = {
            self.Meta.geo_field: feature["geometry"],
            "metadata": feature["properties"],
        }

        if self.Meta.bbox_geo_field and "bbox" in feature:
            attrs[self.Meta.bbox_geo_field] = Polygon.from_bbox(feature["bbox"])

        return attrs


class TabularDatasetSerializer(serializers.ModelSerializer):
    cluster = serializers.ReadOnlyField(source="cluster.name")

    class Meta:
        model = TabularDataset
        fields = ["id", "name", "created", "updated", "cluster", "type", "source"]


class TabularItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = TabularItem
        fields = ["id", "data"]

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        # Extract the data field and merge it with the top level fields
        data_content = representation.pop("data", {})

        return {**representation, **data_content}


class TabularItemExcelSerializer(serializers.ModelSerializer):
    # Dynamically add fields based on all possible keys in the data
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Get all possible keys from the queryset
        if self.context.get("view"):
            queryset = self.context["view"].get_queryset()
            all_keys = set()
            for item in queryset:
                if item.data and isinstance(item.data, dict):
                    all_keys.update(item.data.keys())

            # Create a field for each key
            for key in all_keys:
                self.fields[key] = serializers.CharField(
                    source=f"data.{key}", required=False, allow_blank=True, default=""
                )

    class Meta:
        model = TabularItem
        fields = ["id"]
