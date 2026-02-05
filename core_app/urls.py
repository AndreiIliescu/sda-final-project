"""
URL configuration for core_app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from restaurant_app import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path("", views.home_page, name="home"),
    path("despre/", views.about_us_page, name="about_us"),
    path("meniu/", views.menu_page, name="menu"),
    path("contact/", views.contact_us_page, name="contact_us"),
    
    path("reclamatii/", views.complaints_and_notifcations_page, name="complaints"),
    path("plati-si-livrare/", views.payments_and_delivery_page, name="payments"),
    path("valori-nutritionale/", views.allergen_and_nutritional_values_page, name="allergens"),
    path("termeni-si-conditii/", views.terms_and_conditions_page, name="terms"),
    path("politica-confidentialitate/", views.privacy_policy_page, name="privacy"),
    path("politica-cookies/", views.cookies_policy_page, name="cookies"),
    path("securitatea-datelor/", views.data_security_page, name="data"),
    path("datele-companiei/", views.company_identification_data_page, name="company"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
