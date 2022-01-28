from django.contrib import admin

from seasonal.models import (
    Idmc,
    IdmcSuddenOnset,
    InformRisk,
    InformRiskSeasonal,
    DisplacementData,
    GarHazardDisplacement,
    GarHazard,
    Ipc,
    IpcMonthly,
    GlobalDisplacement,
    ThinkHazardCountry,
    ThinkHazardInformation,
)


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


@admin.register(Ipc)
class IpcAdmin(admin.ModelAdmin):
    pass


@admin.register(IpcMonthly)
class IpcMonthly(admin.ModelAdmin):
    pass


@admin.register(GlobalDisplacement)
class GlobalDisplacement(admin.ModelAdmin):
    pass


@admin.register(ThinkHazardCountry)
class ThinkHazardCountry(admin.ModelAdmin):
    pass


@admin.register(ThinkHazardInformation)
class ThinkHazardInformation(admin.ModelAdmin):
    pass
