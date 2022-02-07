from django.contrib import admin

from common.models import Country, Region


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    pass


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    pass
