"""
URL configuration for unrols project.

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
from django.contrib.sitemaps.views import sitemap, index
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from core.views import maintenance as maintenance_view
from core.sitemaps import *

sitemaps = {
    "pages": MainSitemap,
    "products": ProductsSitemap
}

if settings.MAINTENANCE:
    urlpatterns = [
        path('', maintenance_view, name='maintenance_page'),
        path('admin/', admin.site.urls),

    ]
else:
    urlpatterns = [
        path('admin/', admin.site.urls),
        path('', include('core.urls')),
        # path('accounts/', include('accounts.urls'))
        path('api/', include('api.urls')),

        path(
            "sitemap.xml",
            index, 
            {'sitemaps': sitemaps},
            name='django.contrib.sitemaps.views.index',
            ),
        path(
            'sitemap_<section>.xml',
            sitemap,
            {"sitemaps": sitemaps},
            name='django.contrib.sitemaps.views.sitemap',
        ),
    ]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
