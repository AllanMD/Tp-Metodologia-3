"""tp_metodologia3 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path
from rent import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home),
    path('city/<int:city_id>', views.home),
    path('signup', views.signup),
    path('login', views.login),
    path('logout', views.logout),
    path('addProperty', views.propertyForm),
    path('property/<int:property_id>', views.property),
    path('admin/', admin.site.urls),
    path('property/<int:property_id>', views.property),
    path('reservation_detail/<int:reservation_id>', views.reservation),
    path('reservations', views.reservations)
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
