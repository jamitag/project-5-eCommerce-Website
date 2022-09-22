from django.contrib import admin
from django.urls import path, include
from .settings import MEDIA_URL, MEDIA_ROOT
from django.conf.urls.static import static
from .views import handler404
from django.views.static import serve as mediaserve
from django.conf.urls import url

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("accounts.urls")),
    path("", include("home.urls")),
    path("products/", include("products.urls")),
    path("order/", include("order.urls")),
    path("payment/", include("checkout.urls")),
]

urlpatterns.append(url(f'^{MEDIA_URL.lstrip("/")}(?P<path>.*)$',
                   mediaserve, {'document_root': MEDIA_ROOT}))

handler404 = 'cycle_store.views.handler404'
