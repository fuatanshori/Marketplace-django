from django.contrib import admin
from .models import Payment,Order,OrderProduct

# Register your models here.
class OrderProductInline(admin.TabularInline):
    model = OrderProduct
    extra=0
    readonly_fields=('payment','user','product','quantity','product_price','ordered')
class OrderAdmin(admin.ModelAdmin):
    list_display=['id','order_number','full_name','email','phone','city','order_total','tax','status','is_ordered','created_at']
    list_filter=['status','is_ordered']
    list_display_links=['order_number']
    search_fields=['order_number','first_name','last_name','phone','email']
    list_per_page=20
    inlines = [OrderProductInline]

admin.site.register(Payment)
admin.site.register(Order,OrderAdmin)
admin.site.register(OrderProduct)