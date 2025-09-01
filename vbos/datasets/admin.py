import csv
from io import TextIOWrapper

from django.contrib.gis import admin
from django.contrib import messages
from django.shortcuts import render, redirect, reverse
from django.urls import path

from .models import (
    RasterDataset,
    TabularDataset,
    TabularItem,
    VectorDataset,
    VectorItem,
)
from .forms import CSVUploadForm


@admin.register(RasterDataset)
class RasterDatasetAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "created", "updated", "file_path"]


@admin.register(VectorDataset)
class VectorDatasetAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "created", "updated"]


@admin.register(VectorItem)
class VectorItemAdmin(admin.GISModelAdmin):
    list_display = ["id", "metadata"]


@admin.register(TabularDataset)
class TabularDatasetAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "created", "updated"]


@admin.register(TabularItem)
class TabularItemAdmin(admin.GISModelAdmin):
    list_display = ["id", "dataset", "data"]

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "upload-file/",
                self.admin_site.admin_view(self.import_file),
                name="datasets_tabularitem_import_file",
            ),
        ]
        return custom_urls + urls

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context["upload_file"] = reverse("admin:datasets_tabularitem_import_file")
        return super().changelist_view(request, extra_context=extra_context)

    def import_file(self, request):
        if request.method == "POST":
            form = CSVUploadForm(request.POST, request.FILES)
            if form.is_valid():
                uploaded_file = request.FILES["file"]

                # Check if the file is a CSV
                if not uploaded_file.name.endswith(".csv"):
                    messages.error(request, "Please upload a CSV file")
                    return redirect("admin:datasets_tabularitem_import_file")

                try:
                    # Read and process the CSV
                    decoded_file = TextIOWrapper(uploaded_file.file, encoding="utf-8")
                    reader = csv.DictReader(decoded_file)

                    created_count = 0
                    error_count = 0

                    for row in reader:  # start=2 to account for header row
                        try:
                            TabularItem.objects.create(
                                dataset=form.cleaned_data["dataset"], data=row
                            )
                            created_count += 1
                        except Exception as e:
                            print(e)
                            error_count += 1

                    if created_count > 0:
                        messages.success(
                            request, f"Successfully created {created_count} new records"
                        )

                    if error_count > 0:
                        messages.warning(request, f"Failed to create {error_count} items.")

                except Exception as e:
                    messages.error(request, f"Error processing CSV: {str(e)}")

                return redirect("admin:datasets_tabularitem_import_file")
        else:
            form = CSVUploadForm()

        context = {
            "form": form,
            "opts": self.model._meta,
            "title": "Import CSV File",
        }
        return render(request, "admin/file_upload.html", context)
