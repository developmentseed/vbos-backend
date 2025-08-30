from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse

from ..models import RasterDataset


class TestRasterDatasetListDetailViews(APITestCase):
    def setUp(self):
        self.dataset_1 = RasterDataset.objects.create(
            name="Rainfall", file_path="cogs/rainfall.tiff"
        )
        self.dataset_2 = RasterDataset.objects.create(
            name="Coastline changes", file_path="cogs/coastlines.tiff"
        )
        self.url = reverse("datasets:raster-list")

    def test_raster_datasets_list(self):
        req = self.client.get(self.url)
        assert req.status_code == status.HTTP_200_OK
        assert req.data.get("count") == 2
        assert req.data.get("results")[0]["name"] == "Rainfall"
        assert req.data.get("results")[1]["name"] == "Coastline changes"

    def test_raster_datasets_detail(self):
        url = reverse("datasets:raster-detail", args=[self.dataset_1.id])
        req = self.client.get(url)
        assert req.status_code == status.HTTP_200_OK
        assert req.data.get("name") == "Rainfall"
        assert req.data.get("file_path") == "cogs/rainfall.tiff"
        assert req.data.get("created")
        assert req.data.get("updated")
