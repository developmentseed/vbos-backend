import io

from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from vbos.datasets.models import TabularDataset, TabularItem


class TabularItemAdminImportFileTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin", password="password", email="admin@example.com"
        )
        self.client.login(username="admin", password="password")
        self.dataset = TabularDataset.objects.create(name="Test Dataset")
        self.upload_url = reverse("admin:datasets_tabularitem_import_file")

    def test_change_list_has_link_to_import_file(self):
        response = self.client.get(reverse("admin:datasets_tabularitem_changelist"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Import File")

    def test_get_import_file_view(self):
        response = self.client.get(self.upload_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Import CSV File")
        self.assertContains(response, "Import File")
        self.assertContains(response, "Dataset")
        self.assertContains(response, "Test Dataset")

    def test_post_invalid_file_type(self):
        file_data = io.BytesIO(b"not a csv")
        file_data.name = "test.txt"
        response = self.client.post(
            self.upload_url,
            {"file": file_data, "dataset": self.dataset.id},
            follow=True,
        )
        self.assertContains(response, "Please upload a CSV file")

    def test_post_valid_csv_creates_items(self):
        csv_content = "col1,col2\nval1,val2\nval3,val4\n"
        file_data = io.BytesIO(csv_content.encode("utf-8"))
        file_data.name = "test.csv"
        response = self.client.post(
            self.upload_url,
            {"file": file_data, "dataset": self.dataset.id},
            follow=True,
        )
        self.assertContains(response, "Successfully created 2 new records")
        self.assertEqual(TabularItem.objects.count(), 2)
        ti_1 = TabularItem.objects.first()
        self.assertEqual(ti_1.dataset.id, self.dataset.id)
        self.assertEqual(ti_1.data["col1"], "val1")
        self.assertEqual(ti_1.data["col2"], "val2")
        ti_2 = TabularItem.objects.last()
        self.assertEqual(ti_2.dataset.id, self.dataset.id)
        self.assertEqual(ti_2.data["col1"], "val3")
        self.assertEqual(ti_2.data["col2"], "val4")
