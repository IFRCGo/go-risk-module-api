from django.contrib import admin

from earthquake.models import Earthquake


@admin.register(Earthquake)
class EarthquakeAdmin(admin.ModelAdmin):
    pass
