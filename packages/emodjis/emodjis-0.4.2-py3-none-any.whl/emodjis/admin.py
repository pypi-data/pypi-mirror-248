"""Admin view for API stats."""

import csv
import zipfile
from django.contrib import admin
from django.utils.timezone import now
from django.http import HttpResponse

from .models import Emoji


class ExportCsvMixin:
    def export_as_csv(self, request, queryset):
        meta = self.model._meta

        response = HttpResponse(content_type="text/csv")
        response[
            "Content-Disposition"
        ] = f"attachment; filename={meta}-{now().strftime('%Y%m%d')}.zip"
        writer = csv.writer(response)

        writer.writerow(self.model.EXPORT_FIELDS)
        for obj in queryset:
            writer.writerow(
                [getattr(obj, field) for field in self.model.EXPORT_FIELDS]
            )

        return response

    export_as_csv.short_description = "Export metadata as CSV"


class ExportZipMixin:
    def export_as_zip(self, request, queryset):
        meta = self.model._meta
        response = HttpResponse(content_type="application/zip")
        response[
            "Content-Disposition"
        ] = f"attachment; filename={meta}-{now().strftime('%Y%m%d')}.zip"
        zip_file = zipfile.ZipFile(response, "w")
        for obj in queryset:
            zip_file.writestr(
                f"{obj.name}.gif",
                obj.image,
            )

        return response

    export_as_zip.short_description = "Export metadata and files as ZIP"


class EmojiAdmin(admin.ModelAdmin, ExportCsvMixin, ExportZipMixin):
    actions = ["export_as_csv", "export_as_zip"]

    list_per_page = 20
    list_display = (
        "name",
        "team",
        "private",
        "nsfw",
        "uses",
        "created_at",
        "created_by",
        "deleted_at",
        "deleted_by",
    )

    fields = (
        "name",
        "team",
        "nsfw",
        "private",
        "uses",
        "created_by",
        "created_at",
        "deleted_at",
        "deleted_by",
    )
    list_filter = ("name", "uses", "nsfw", "private")
    search_fields = ("name",)
    readonly_fields = (
        "created_at",
        "created_by",
        "deleted_at",
        "deleted_by",
        "image",
        "uses",
    )

    change_list_template = "charts_change_list.html"

    def get_queryset(self, request):
        if request.user.is_superuser:
            return Emoji.admin.all()
        else:
            return Emoji.updates.nsfw(user=request.user)

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(request, extra_context)
        try:
            filtered_query_set = response.context_data["cl"].queryset
        except KeyError:
            return response
        usage = filtered_query_set.values("name", "image", "uses").order_by(
            "-uses", "name"
        )[:10]
        extra_context = dict(usage=usage)
        response.context_data.update(extra_context)
        return response

    def changeform_view(
        self, request, object_id=None, form_url="", extra_context=None
    ):
        if request.GET.get("export_csv", False):
            export_queryset = self.get_queryset(request).filter(pk=object_id)
            return self.export_as_csv(request, export_queryset)
        if request.GET.get("export_zip", False):
            export_queryset = self.get_queryset(request).filter(pk=object_id)
            return self.export_as_csv(request, export_queryset)
        return super().changeform_view(
            request, object_id, form_url, extra_context
        )

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if obj:
            return request.user == obj.created_by or request.user.is_superuser
        return False


admin.site.register(Emoji, EmojiAdmin)
