from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse

from ..models import TabularDataset, TabularItem
from ...users.test.factories import UserFactory


class TestTabularDatasetListDetailViews(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.dataset_1 = TabularDataset.objects.create(name="Population")
        self.dataset_2 = TabularDataset.objects.create(name="Prices")
        self.url = reverse("datasets:tabular-list")

    def test_tabular_datasets_list(self):
        req = self.client.get(self.url)
        assert req.status_code == status.HTTP_200_OK
        assert req.data.get("count") == 2
        assert req.data.get("results")[0]["name"] == "Population"
        assert req.data.get("results")[1]["name"] == "Prices"

    def test_tabular_datasets_detail(self):
        url = reverse("datasets:tabular-detail", args=[self.dataset_1.id])
        req = self.client.get(url)
        assert req.status_code == status.HTTP_200_OK
        assert req.data.get("name") == "Population"
        assert req.data.get("created")
        assert req.data.get("updated")


class TestTabularDatasetDataView(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.dataset_1 = TabularDataset.objects.create(name="Population")
        self.dataset_2 = TabularDataset.objects.create(name="Employment")
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
            data={"employed_population": 0.75, "year": 2025, "month": 1},
        )
        TabularItem.objects.create(
            dataset=self.dataset_2,
            data={"employed_population": 0.85, "year": 2024, "month": 7},
        )
        TabularItem.objects.create(
            dataset=self.dataset_2,
            data={"employed_population": 0.82, "year": 2024, "month": 1},
        )
        TabularItem.objects.create(
            dataset=self.dataset_2,
            data={"employed_population": 0.80, "year": 2023, "month": 7},
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
