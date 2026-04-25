from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("auth/", include("users.urls")),
    path("wallet/", include("wallet.urls")),
    path("card/", include("cards.urls")),
    path("transactions/", include("transactions.urls")),
]
