"""
URL configuration for main project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from rest_framework import routers
from django.conf import settings
from django.conf.urls.static import static
router = routers.DefaultRouter()

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include('languagecards.urls',)),
    path("__debug__/", include("debug_toolbar.urls")),
    path('', include(router.urls)),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    path("favicon.ico", RedirectView.as_view(url=settings.STATIC_URL + "img/favicon.ico")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
