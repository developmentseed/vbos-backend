from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse

from ..models import Cluster, TabularDataset, TabularItem
from ...users.test.factories import UserFactory


class TestTabularDatasetListDetailViews(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.dataset_1 = TabularDataset.objects.create(
            name="Population",
            cluster=Cluster.objects.create(name="Administrative"),
            source="Government",
        )
        self.dataset_2 = TabularDataset.objects.create(
            name="Prices",
            cluster=Cluster.objects.create(name="Statistics"),
            source="Government",
            type="estimated_damage",
        )
        self.url = reverse("datasets:tabular-list")

    def test_tabular_datasets_list(self):
        req = self.client.get(self.url)
        assert req.status_code == status.HTTP_200_OK
        assert req.data.get("count") == 2
        assert req.data.get("results")[0]["name"] == "Population"
        assert req.data.get("results")[1]["name"] == "Prices"
        assert req.data.get("results")[0]["source"] == "Government"
        assert req.data.get("results")[1]["source"] == "Government"
        assert req.data.get("results")[0]["cluster"] == "Administrative"
        assert req.data.get("results")[1]["cluster"] == "Statistics"
        assert req.data.get("results")[0]["type"] == "baseline"
        assert req.data.get("results")[1]["type"] == "estimated_damage"

    def test_raster_datasets_list_filter(self):
        req = self.client.get(self.url, {"cluster": "transportation"})
        assert req.status_code == status.HTTP_400_BAD_REQUEST

        req = self.client.get(self.url, {"cluster": "administrative"})
        assert req.status_code == status.HTTP_200_OK
        assert req.data.get("count") == 1

        req = self.client.get(self.url, {"cluster": "statistics"})
        assert req.status_code == status.HTTP_200_OK
        assert req.data.get("count") == 1

    def test_tabular_datasets_detail(self):
        url = reverse("datasets:tabular-detail", args=[self.dataset_1.id])
        req = self.client.get(url)
        assert req.status_code == status.HTTP_200_OK
        assert req.data.get("name") == "Population"
        assert req.data.get("created")
        assert req.data.get("updated")


class TestTabularDatasetDataView(APITestCase):
    def setUp(self):
        self.cluster = Cluster.objects.create(name="Other")
        self.user = UserFactory()
        self.dataset_1 = TabularDataset.objects.create(
            name="Population", cluster=self.cluster
        )
        self.dataset_2 = TabularDataset.objects.create(
            name="Employment", cluster=self.cluster
        )
        self.item = TabularItem.objects.create(
            dataset=self.dataset_1,
            data={"province": "A", "population": 1902, "year": 2025},
        )
        TabularItem.objects.create(
            dataset=self.dataset_1,
            data={"province": "B", "population": 10902, "year": 2025},
        )
        TabularItem.objects.create(
            dataset=self.dataset_1,
            data={"province": "C", "population": 875, "year": 2025},
        )
        TabularItem.objects.create(
            dataset=self.dataset_2,
            data={
                "employed_population": 0.75,
                "year": 2025,
                "month": 1,
                "region": "North",
            },
        )
        TabularItem.objects.create(
            dataset=self.dataset_2,
            data={
                "employed_population": 0.85,
                "year": 2024,
                "month": 7,
                "region": "North",
            },
        )
        TabularItem.objects.create(
            dataset=self.dataset_2,
            data={
                "employed_population": 0.82,
                "year": 2024,
                "month": 1,
                "region": "South",
            },
        )
        TabularItem.objects.create(
            dataset=self.dataset_2,
            data={
                "employed_population": 0.80,
                "year": 2023,
                "month": 7,
                "region": "East",
            },
        )
        self.url = reverse("datasets:tabular-data", args=[self.dataset_1.id])

    def test_tabular_datasets_data(self):
        req = self.client.get(self.url)
        assert req.status_code == status.HTTP_200_OK
        assert req.data.get("count") == 3
        assert len(req.data.get("results")) == 3
        assert req.data.get("results")[0]["province"] == "A"
        assert req.data.get("results")[0]["population"] == 1902
        assert req.data.get("results")[0]["year"] == 2025

        # fetch second dataset's data
        url = reverse("datasets:tabular-data", args=[self.dataset_2.id])
        req = self.client.get(url)
        assert req.status_code == status.HTTP_200_OK
        assert req.data.get("count") == 4
        assert len(req.data.get("results")) == 4
        assert req.data.get("results")[0]["employed_population"] == 0.75
        assert req.data.get("results")[0]["month"] == 1
        assert req.data.get("results")[0]["year"] == 2025

    def test_filter_data(self):
        url = reverse("datasets:tabular-data", args=[self.dataset_2.id])
        req = self.client.get(url, {"filter": "year=2024"})
        assert req.status_code == status.HTTP_200_OK
        assert req.data.get("count") == 2

        req = self.client.get(url, {"filter": "year=2024,month=1"})
        assert req.status_code == status.HTTP_200_OK
        assert req.data.get("count") == 1

        req = self.client.get(url, {"filter": "year__gte=2024,region__icontains=south"})
        assert req.status_code == status.HTTP_200_OK
        assert req.data.get("count") == 1

        req = self.client.get(url, {"filter": "region__icontains=north"})
        assert req.status_code == status.HTTP_200_OK
        assert req.data.get("count") == 2
