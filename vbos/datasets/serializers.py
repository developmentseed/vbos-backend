from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer

from .models import VectorDataset, VectorItem


class VectorDatasetSerializer(serializers.ModelSerializer):
    class Meta:
        model = VectorDataset
        fields = "__all__"


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
