from django.contrib import admin
from .models import Category
# Register your models here.
class ReadOnlyAdmin(admin.ModelAdmin):
    list_display=['category_name','slug']
    list_display_links=['category_name']
    readonly_fields=[
        'slug'
    ]
admin.site.register(Category,ReadOnlyAdmin)