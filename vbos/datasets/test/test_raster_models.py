from django.db.models.deletion import ProtectedError
from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.exceptions import ValidationError

from vbos.datasets.models import RasterDataset, RasterFile
from genericpath import exists


class TestRasterModels(TestCase):
    def setUp(self):
        self.valid_file = SimpleUploadedFile(
            "rainfall.tif", b"file_content", content_type="image/tiff"
        )
        self.r_1 = RasterFile.objects.create(name="Rainfall COG", file=self.valid_file)
        self.r_2 = RasterFile.objects.create(
            name="Coastline COG", file="raster/coastline.tiff"
        )
        self.dataset = RasterDataset.objects.create(name="Rainfall", file=self.r_1)

    def test_deletion(self):
        # RasterFile can't be deleted if it's associates with a dataset
        with self.assertRaises(ProtectedError):
            self.r_1.delete()
        # modify dataset
        self.dataset.file = self.r_2
        self.dataset.save()
        # delete file
        self.r_1.delete()
        self.assertEqual(RasterFile.objects.count(), 1)
        # delete dataset
        self.dataset.delete()
        self.assertEqual(RasterDataset.objects.count(), 0)
        # delete remaining file
        self.r_2.delete()
        self.assertEqual(RasterFile.objects.count(), 0)

        # test file extension validation
        invalid_file = SimpleUploadedFile(
            "test.jpg", b"file_content", content_type="image/jpeg"
        )
        raster = RasterFile(name="Test", file=invalid_file)
        with self.assertRaises(ValidationError):
            raster.full_clean()
