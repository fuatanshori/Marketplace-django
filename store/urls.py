from django.urls import path
from .import views 

urlpatterns = [
    path('',views.store,name='store'),
    path('category/<slug:category_input>/',views.store,name='products_by_category'),
    path('category/<slug:category_input>/<slug:product_input>/',views.product_detail,name='product_detail'),
    path('search/',views.search,name='search'),
    path('data/',views.alldata,name='data'),
    path('export_excel/',views.export_excel,name='export_excel'),
]