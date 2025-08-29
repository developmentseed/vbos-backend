from django.shortcuts import render
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework_gis.pagination import GeoJsonPagination

from .models import VectorDataset, VectorItem
from .pagination import StandardResultsSetPagination
from .serializers import VectorDatasetSerializer, VectorItemSerializer


class VectorDatasetListView(ListAPIView):
    queryset = VectorDataset.objects.all()
    serializer_class = VectorDatasetSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = StandardResultsSetPagination


class VectorDatasetDetailView(RetrieveAPIView):
    queryset = VectorDataset.objects.all()
    serializer_class = VectorDatasetSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class VectorDatasetDataView(ListAPIView):
    serializer_class = VectorItemSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = GeoJsonPagination

    def get_queryset(self):
        return VectorItem.objects.filter(dataset=self.kwargs.get("pk"))
