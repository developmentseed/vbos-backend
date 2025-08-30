from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.gis.geos import Polygon, LineString, Point

from ..models import VectorDataset, VectorItem


class TestVectorDatasetListDetailViews(APITestCase):
    def setUp(self):
        self.dataset_1 = VectorDataset.objects.create(name="Boundaries")
        self.dataset_2 = VectorDataset.objects.create(name="Roads")
        self.url = reverse("datasets:vector-list")

    def test_vector_datasets_list(self):
        req = self.client.get(self.url)
        assert req.status_code == status.HTTP_200_OK
        assert req.data.get("count") == 2
        assert req.data.get("results")[0]["name"] == "Boundaries"
        assert req.data.get("results")[1]["name"] == "Roads"

    def test_vector_datasets_detail(self):
        url = reverse("datasets:vector-detail", args=[self.dataset_1.id])
        req = self.client.get(url)
        assert req.status_code == status.HTTP_200_OK
        assert req.data.get("name") == "Boundaries"
        assert req.data.get("created")
        assert req.data.get("updated")


class TestVectorDatasetDataView(APITestCase):
    def setUp(self):
        self.dataset_1 = VectorDataset.objects.create(name="Boundaries")
        self.dataset_2 = VectorDataset.objects.create(name="Roads")
        VectorItem.objects.create(
            dataset=self.dataset_1,
            geometry=Point(80.5, 10.232),
            metadata={"type": "administrative", "name": "Point 1"},
        )
        VectorItem.objects.create(
            dataset=self.dataset_1,
            geometry=LineString([(0, 0), (0, 3), (3, 3), (3, 0), (6, 6), (0, 0)]),
            metadata={"type": "administrative", "name": "Line 123"},
        )
        VectorItem.objects.create(
            dataset=self.dataset_2,
            geometry=Polygon([(0, 0), (0, 3), (3, 3), (3, 0), (0, 0)]),
            metadata={"type": "administrative", "name": "Area 1"},
        )
        self.url = reverse("datasets:vector-data", args=[self.dataset_1.id])

    def test_vector_datasets_data(self):
        req = self.client.get(self.url)
        assert req.status_code == status.HTTP_200_OK
        assert req.data.get("count") == 2
        assert len(req.data.get("features")) == 2
        assert req.data.get("features")[0]["geometry"] == {
            "type": "Point",
            "coordinates": [80.5, 10.232],
        }
        assert req.data.get("features")[0]["properties"]["name"] == "Point 1"
        assert req.data.get("features")[0]["properties"]["type"] == "administrative"

        # fetch second dataset's data
        url = reverse("datasets:vector-data", args=[self.dataset_2.id])
        req = self.client.get(url)
        assert req.status_code == status.HTTP_200_OK
        assert req.data.get("count") == 1
        assert len(req.data.get("features")) == 1
        assert req.data.get("features")[0]["geometry"] == {
            "type": "Polygon",
            "coordinates": [
                [[0.0, 0.0], [0.0, 3.0], [3.0, 3.0], [3.0, 0.0], [0.0, 0.0]]
            ],
        }

    def test_filters(self):
        req = self.client.get(self.url, {"in_bbox": "80,10,81,11"})
        assert req.status_code == status.HTTP_200_OK
        assert req.data.get("count") == 1
        assert len(req.data.get("features")) == 1
        assert req.data.get("features")[0]["geometry"] == {
            "type": "Point",
            "coordinates": [80.5, 10.232],
        }
        assert req.data.get("features")[0]["properties"]["name"] == "Point 1"
