from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("core.urls")),      # our app
    path("accounts/", include("django.contrib.auth.urls")),  # login/logout
]
