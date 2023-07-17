"""risk_module URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.conf.urls import url, include
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from seasonal.views import (
    SeasonalViewSet,
    EarlyActionViewSet,
    PublishReportViewSet,
    RiskScoreViewSet,
    InformScoreViewSet,
    SeasonalCountryViewSet,
    generate_data,
)
from imminent.views import (
    OddrinViewSet,
    EarthquakeViewSet,
    AdamViewSet,
    PdcViewSet,
    GDACSViewSet,
    MeteoSwissViewSet,
    GWISViewSet,
)

from rest_framework import routers


router = routers.DefaultRouter()

router.register(r'earthquake', EarthquakeViewSet, basename='earthquake')
router.register(r'global-exposure-data', OddrinViewSet, basename='oddrin')
router.register(r'seasonal', SeasonalViewSet, basename='seasonal')
router.register(r'country-seasonal', SeasonalCountryViewSet, basename='seasonal country')
router.register(r'imminent', PdcViewSet, basename='imminent')

router.register(r'early-actions', EarlyActionViewSet, basename='early actions')
router.register(r'publish-report', PublishReportViewSet, basename='publish report')
router.register(r'risk-score', RiskScoreViewSet, basename='risk score')
router.register(r'adam-exposure', AdamViewSet, basename='adam exposure')
router.register(r'inform-score', InformScoreViewSet, basename='infom score')
router.register(r'gdacs', GDACSViewSet, basename='gdacs')
router.register(r'meteoswiss', MeteoSwissViewSet, basename='meteoswiss')
router.register(r'gwis', GWISViewSet, basename='gwis')

urlpatterns = [
    url(r'^api/v1/', include(router.urls)),
    path('admin/', admin.site.urls),
    path(r'api/v1/export', generate_data),
    # Docs
    path("docs/", SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    path("api-docs/", SpectacularAPIView.as_view(), name='schema'),
    path("api-docs/swagger-ui/", SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
