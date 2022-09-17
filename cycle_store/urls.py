from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import handler404

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("accounts.urls")),
    path("", include("home.urls")),
    path("products/", include("products.urls")),
    path("order/", include("order.urls")),
    path("payment/", include("checkout.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'cycle_store.views.handler404'