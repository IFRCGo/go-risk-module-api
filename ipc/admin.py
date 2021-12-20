from django.contrib import admin

from ipc.models import (
    Ipc,
    IpcMonthly,
    Country,
    GlobalDisplacement,
    ThinkHazardCountry,
    ThinkHazardInformation
)


@admin.register(Ipc)
class IpcAdmin(admin.ModelAdmin):
    pass


@admin.register(IpcMonthly)
class IpcMonthly(admin.ModelAdmin):
    pass


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
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
