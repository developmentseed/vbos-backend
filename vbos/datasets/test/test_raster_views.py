from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse

from ..models import Cluster, RasterDataset, RasterFile


class TestRasterDatasetListDetailViews(APITestCase):
    def setUp(self):
        self.r_1 = RasterFile.objects.create(
            name="Rainfall COG", file="raster/rainfall.tiff"
        )
        self.r_2 = RasterFile.objects.create(
            name="Coastline COG", file="raster/coastline.tiff"
        )
        self.dataset_1 = RasterDataset.objects.create(
            name="Rainfall",
            cluster=Cluster.objects.create(name="Environment"),
            file=self.r_1,
            source="WMO",
        )
        self.dataset_2 = RasterDataset.objects.create(
            name="Coastline changes",
            file=self.r_2,
            source="OSM",
            cluster=Cluster.objects.create(name="Administrative"),
        )
        self.url = reverse("datasets:raster-list")

    def test_raster_datasets_list(self):
        req = self.client.get(self.url)
        assert req.status_code == status.HTTP_200_OK
        assert req.data.get("count") == 2
        assert req.data.get("results")[0]["name"] == "Rainfall"
        assert req.data.get("results")[1]["name"] == "Coastline changes"
        assert req.data.get("results")[0]["cluster"] == "Environment"
        assert req.data.get("results")[1]["cluster"] == "Administrative"
        assert req.data.get("results")[0]["source"] == "WMO"
        assert req.data.get("results")[1]["source"] == "OSM"

    def test_raster_datasets_list_filter(self):
        req = self.client.get(self.url, {"cluster": "transportation"})
        assert req.status_code == status.HTTP_400_BAD_REQUEST

        req = self.client.get(self.url, {"cluster": "administrative"})
        assert req.status_code == status.HTTP_200_OK
        assert req.data.get("count") == 1

        req = self.client.get(self.url, {"cluster": "environment"})
        assert req.status_code == status.HTTP_200_OK
        assert req.data.get("count") == 1

    def test_raster_datasets_detail(self):
        url = reverse("datasets:raster-detail", args=[self.dataset_1.id])
        req = self.client.get(url)
        assert req.status_code == status.HTTP_200_OK
        assert req.data.get("name") == "Rainfall"
        assert req.data.get("file") == "/media/raster/rainfall.tiff"
        assert req.data.get("created")
        assert req.data.get("updated")
        assert req.data.get("source") == "WMO"
        assert req.data.get("cluster") == "Environment"
