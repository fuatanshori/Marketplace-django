from django.contrib import admin
from .models import Products,Variation,ReviewRating


# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name','price','stock','category','created_date')
    readonly_fields=[
        'slug'
    ]
class VariationAdmin(admin.ModelAdmin):
    list_display = ('product','variation_category','variation_value','is_active','created_date')
    list_editable=['is_active']
    list_filter=[
        'product','variation_category','variation_value'
    ]
admin.site.register(Products,ProductAdmin)
admin.site.register(Variation,VariationAdmin)
admin.site.register(ReviewRating)