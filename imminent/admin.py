from django.contrib import admin

from imminent.models import (
    Oddrin,
    Pdc,
    PdcDisplacement,
    Earthquake,
    Adam
)


@admin.register(Oddrin)
class OddrinAdmin(admin.ModelAdmin):
    pass


@admin.register(Pdc)
class PdcdAdmin(admin.ModelAdmin):
    pass


@admin.register(PdcDisplacement)
class PdcDisplacementdAdmin(admin.ModelAdmin):
    pass


@admin.register(Earthquake)
class EarthquakeAdmin(admin.ModelAdmin):
    pass


@admin.register(Adam)
class AdamAdmin(admin.ModelAdmin):
    pass
