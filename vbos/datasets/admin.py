from django.contrib.gis import admin
from .models import (
    RasterDataset,
    TabularDataset,
    TabularItem,
    VectorDataset,
    VectorItem,
)


@admin.register(RasterDataset)
class RasterDatasetAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "created", "updated", "file_path"]


@admin.register(VectorDataset)
class VectorDatasetAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "created", "updated"]


@admin.register(VectorItem)
class VectorItemAdmin(admin.GISModelAdmin):
    list_display = ["id", "metadata"]


@admin.register(TabularDataset)
class TabularDatasetAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "created", "updated"]


@admin.register(TabularItem)
class TabularItemAdmin(admin.GISModelAdmin):
    list_display = ["id", "data"]
