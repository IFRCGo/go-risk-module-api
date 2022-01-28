from django.contrib import admin

from common.models import Country


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    pass
