from django.db.models.deletion import ProtectedError
from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.exceptions import ValidationError

from vbos.datasets.models import Cluster, RasterDataset, RasterFile


class TestRasterModels(TestCase):
    def setUp(self):
        self.valid_file = SimpleUploadedFile(
            "rainfall.tiff", b"file_content", content_type="image/tiff"
        )
        self.r_1 = RasterFile.objects.create(name="Rainfall COG", file=self.valid_file)
        self.r_2 = RasterFile.objects.create(
            name="Coastline COG", file="raster/coastline.tiff"
        )
        self.dataset = RasterDataset.objects.create(
            name="Rainfall",
            cluster=Cluster.objects.create(name="Environment"),
            file=self.r_1,
        )

    def test_deletion(self):
        # RasterFile can't be deleted if it's associates with a dataset
        with self.assertRaises(ProtectedError):
            self.r_1.delete()

        # name should be unique
        raster = RasterFile(name="Rainfall COG 2", file="raster/coastline.tiff")
        with self.assertRaises(ValidationError):
            raster.full_clean()

        # file path should be unique
        raster = RasterFile(name="Rainfall COG", file="newfile.tif")
        with self.assertRaises(ValidationError):
            raster.full_clean()

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

    def tearDown(self):
        RasterFile.objects.all().delete()
