from django.contrib.gis import admin
from .models import VectorDataset, VectorItem


@admin.register(VectorDataset)
class VectorDatasetAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "created", "updated"]


@admin.register(VectorItem)
class VectorItemAdmin(admin.GISModelAdmin):
    list_display = ["id", "metadata"]
