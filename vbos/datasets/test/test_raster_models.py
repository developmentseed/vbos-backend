from django.db.models.deletion import ProtectedError
from django.test import TestCase

from vbos.datasets.models import RasterDataset, RasterFile


class TestRasterModels(TestCase):
    def setUp(self):
        self.r_1 = RasterFile.objects.create(
            name="Rainfall COG", file="raster/rainfall.tiff"
        )
        self.r_2 = RasterFile.objects.create(
            name="Coastline COG", file="raster/coastline.tiff"
        )
        self.dataset = RasterDataset.objects.create(name="Rainfall", file=self.r_1)

    def test_deletion_restriction(self):
        with self.assertRaises(ProtectedError):
            self.r_1.delete()
        self.r_2.delete()
        self.assertEqual(RasterFile.objects.count(), 1)

    def test_deletion(self):
        self.dataset.file = self.r_2
        self.dataset.save()
        self.r_1.delete()
        self.assertEqual(RasterFile.objects.count(), 1)
        self.dataset.delete()
        self.assertEqual(RasterDataset.objects.count(), 0)
        self.r_2.delete()
        self.assertEqual(RasterFile.objects.count(), 0)
