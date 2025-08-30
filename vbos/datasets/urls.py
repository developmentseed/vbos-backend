from django.urls import path

from . import views

app_name = "datasets"

urlpatterns = [
    # raster
    path("raster/", views.RasterDatasetListView.as_view(), name="raster-list"),
    path(
        "raster/<int:pk>/",
        views.RasterDatasetDetailView.as_view(),
        name="raster-detail",
    ),
    # vector
    path("vector/", views.VectorDatasetListView.as_view(), name="vector-list"),
    path(
        "vector/<int:pk>/",
        views.VectorDatasetDetailView.as_view(),
        name="vector-detail",
    ),
    path(
        "vector/<int:pk>/data/",
        views.VectorDatasetDataView.as_view(),
        name="vector-data",
    ),
    # tabular
    path("tabular/", views.TabularDatasetListView.as_view(), name="tabular-list"),
    path(
        "tabular/<int:pk>/",
        views.TabularDatasetDetailView.as_view(),
        name="tabular-detail",
    ),
    path(
        "tabular/<int:pk>/data/",
        views.TabularDatasetDataView.as_view(),
        name="tabular-data",
    ),
]
