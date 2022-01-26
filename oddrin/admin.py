from django.contrib import admin

from oddrin.models import (
    Oddrin,
    Idmc,
    InformRisk,
    IdmcSuddenOnset,
    InformRiskSeasonal,
    DisplacementData,
    GarHazard,
    Pdc,
    PdcDisplacement,
    GarHazardDisplacement,
)


@admin.register(Oddrin)
class OddrinAdmin(admin.ModelAdmin):
    pass


@admin.register(Idmc)
class IdmcAdmin(admin.ModelAdmin):
    pass


@admin.register(InformRisk)
class InformRiskAdmin(admin.ModelAdmin):
    pass


@admin.register(IdmcSuddenOnset)
class IdmcSuddenOnsetAdmin(admin.ModelAdmin):
    pass


@admin.register(InformRiskSeasonal)
class InformRiskSeasonalAdmin(admin.ModelAdmin):
    pass


@admin.register(DisplacementData)
class DisplacementDataAdmin(admin.ModelAdmin):
    pass


@admin.register(GarHazard)
class GarHazardAdmin(admin.ModelAdmin):
    pass


@admin.register(GarHazardDisplacement)
class GarHazardDisplacementAdmin(admin.ModelAdmin):
    pass


@admin.register(Pdc)
class PdcdAdmin(admin.ModelAdmin):
    pass


@admin.register(PdcDisplacement)
class PdcDisplacementdAdmin(admin.ModelAdmin):
    pass
