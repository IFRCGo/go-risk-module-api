from django.contrib import admin

from imminent.models import (
    Oddrin,
    Pdc,
    PdcDisplacement,
    Earthquake,
    Adam,
    # MeteoSwissFile,
    GDACS,
    MeteoSwiss,
    MeteoSwissAgg,
    GWIS,
)


@admin.register(Oddrin)
class OddrinAdmin(admin.ModelAdmin):
    pass


@admin.register(Pdc)
class PdcdAdmin(admin.ModelAdmin):
    search_fields = ["hazard_name"]


@admin.register(PdcDisplacement)
class PdcDisplacementdAdmin(admin.ModelAdmin):
    autocomplete_fields = ["pdc"]


@admin.register(Earthquake)
class EarthquakeAdmin(admin.ModelAdmin):
    pass


@admin.register(Adam)
class AdamAdmin(admin.ModelAdmin):
    search_fields = ["country__iso3", "country__name"]


# @admin.register(MeteoSwissFile)
# class MeteoSwissFileAdmin(admin.ModelAdmin):
#     pass


@admin.register(GDACS)
class GDACSAdmin(admin.ModelAdmin):
    search_fields = ["country__iso3", "country__name"]


@admin.register(MeteoSwiss)
class MeteoSwissAdmin(admin.ModelAdmin):
    search_fields = ["country__iso3", "country__name"]


@admin.register(MeteoSwissAgg)
class MeteoSwissAggAdmin(admin.ModelAdmin):
    search_fields = ["country__iso3", "country__name"]


@admin.register(GWIS)
class GWISAdmin(admin.ModelAdmin):
    pass
