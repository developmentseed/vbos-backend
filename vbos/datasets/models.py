from django.contrib.gis.db import models


class RasterDataset(models.Model):
    name = models.CharField(max_length=155)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    file_path = models.CharField(max_length=2000, null=False, blank=False)

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
