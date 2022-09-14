from django.contrib import admin
from django.urls import path,include


from .import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls,name='admin'),
    path('',views.home,name='home'),
    path('store/',include(('store.urls','store'))),
    path('carts/',include(('carts.urls','carts'))),
    path('accounts/',include(('accounts.urls','accounts'))),
    path('orders/',include(('orders.urls','orders'))),
]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
