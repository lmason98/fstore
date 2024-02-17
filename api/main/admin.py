from django.contrib import admin

from main.models import Folder, Blob


class FolderAdmin(admin.ModelAdmin):

	list_display = ('owner', 'parent', 'name', 'created_at', 'updated_at')
	search_fields = ('name',)


class BlobAdmin(admin.ModelAdmin):

	list_display = ('owner', 'parent', 'name', 'size', 'created_at', 'updated_at')
	search_fields = ('name',)


admin.site.register(Folder, FolderAdmin)
admin.site.register(Blob, BlobAdmin)

