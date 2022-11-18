from django.contrib import admin

from seasonal.models import (
    Idmc,
    IdmcSuddenOnset,
    InformRisk,
    InformRiskSeasonal,
    DisplacementData,
    GarHazardDisplacement,
    GarHazard,
    GarProbabilistic,
    Ipc,
    IpcMonthly,
    GlobalDisplacement,
    ThinkHazardCountry,
    ThinkHazardInformation,
    PossibleEarlyActions,
    PossibleEarlyActionsSectors,
    PublishReport,
    PublishReportProgram,
    RiskScore
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


@admin.register(GarProbabilistic)
class GarProbabilisticAdmin(admin.ModelAdmin):
    pass


@admin.register(Ipc)
class IpcAdmin(admin.ModelAdmin):
    search_fields = ('country__name', 'analysis_date')


@admin.register(IpcMonthly)
class IpcMonthly(admin.ModelAdmin):
    search_fields = ('country__name', 'analysis_date')


@admin.register(GlobalDisplacement)
class GlobalDisplacement(admin.ModelAdmin):
    pass


@admin.register(ThinkHazardCountry)
class ThinkHazardCountry(admin.ModelAdmin):
    pass


@admin.register(ThinkHazardInformation)
class ThinkHazardInformation(admin.ModelAdmin):
    pass


@admin.register(PossibleEarlyActions)
class PossibleEarlyActionsAdmin(admin.ModelAdmin):
    pass


@admin.register(PossibleEarlyActionsSectors)
class PossibleEarlyActionsSectorsAdmin(admin.ModelAdmin):
    pass


@admin.register(PublishReportProgram)
class PublishReportProgramAdmin(admin.ModelAdmin):
    pass


@admin.register(PublishReport)
class PublishReportAdmin(admin.ModelAdmin):
    pass


@admin.register(RiskScore)
class RiskScore(admin.ModelAdmin):
    pass
