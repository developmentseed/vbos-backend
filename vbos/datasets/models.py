from django.contrib.gis.db import models
from django.db.models.fields.files import default_storage
from django.db.models.signals import pre_delete
from django.dispatch import receiver


class RasterFile(models.Model):
    name = models.CharField(max_length=155)
    created = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to="raster/")

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["id"]


@receiver(pre_delete, sender=RasterFile)
def delete_raster_file(sender, instance, **kwargs):
    """
    Delete the file from storage when a RasterFile instance is deleted
    """
    if instance.file:
        # Using default_storage for better compatibility with different storage backends
        if default_storage.exists(instance.file.name):
            default_storage.delete(instance.file.name)


class RasterDataset(models.Model):
    name = models.CharField(max_length=155)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    file = models.ForeignKey(RasterFile, on_delete=models.PROTECT)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["id"]


class VectorDataset(models.Model):
    name = models.CharField(max_length=155)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["id"]


class VectorItem(models.Model):
    dataset = models.ForeignKey(VectorDataset, on_delete=models.CASCADE)
    geometry = models.GeometryField()
    metadata = models.JSONField(default=dict, blank=True, null=True)

    def __str__(self):
        return f"{self.id}"

    class Meta:
        ordering = ["id"]


class TabularDataset(models.Model):
    name = models.CharField(max_length=155)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["id"]


class TabularItem(models.Model):
    dataset = models.ForeignKey(TabularDataset, on_delete=models.CASCADE)
    data = models.JSONField(default=dict)

    def __str__(self):
        return f"{self.id}"

    class Meta:
        ordering = ["id"]
