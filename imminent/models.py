from django.db import models
from django.utils.translation import ugettext_lazy as _

from common.models import Country, HazardType


class Oddrin(models.Model):
    class FileType(models.TextChoices):
        RASTER = "raster", "Raster"
        VECTOR = "vector", "Vector"

    class DataSource(models.TextChoices):
        ODDRIN = "oddrin", "Oddrin"
        PACIFIC_DIASATER_CENTER = "pdc", "Pdc"

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    hazard_title = models.CharField(max_length=255, verbose_name=_("hazard title"))
    hazard_type = models.CharField(max_length=100, verbose_name=_("hazard type"), choices=HazardType.choices, blank=True)
    source_type = models.CharField(max_length=100, verbose_name=_("source type"), choices=DataSource.choices, blank=True)
    glide_number = models.CharField(max_length=100, verbose_name=_("glide number"), null=True, blank=True)
    uuid = models.CharField(max_length=128, verbose_name=_("uuid"), null=True, blank=True)
    latitude = models.FloatField(verbose_name=_("latitude"), null=True, blank=True)
    longitude = models.FloatField(verbose_name=_("longitude"), null=True, blank=True)
    iso3 = models.CharField(max_length=3, verbose_name=_("iso3"), null=True, blank=True)
    people_exposed = models.IntegerField(verbose_name=_("people exposed"), null=True, blank=True)
    people_displaced = models.IntegerField(verbose_name=_("people displaced"), null=True, blank=True)
    buildings_exposed = models.IntegerField(verbose_name=_("buildings exposed"), null=True, blank=True)
    lower_displacement = models.IntegerField(verbose_name=_("lower displacement"), null=True, blank=True)
    higher_displacement = models.IntegerField(verbose_name=_("higher displacement"), null=True, blank=True)
    file = models.FileField(verbose_name=_("file"), blank=True, null=True, upload_to="oddrin/files")
    cog_file = models.FileField(verbose_name=_("cog file"), blank=True, null=True, upload_to="oddrin/cog_files")
    file_type = models.CharField(max_length=100, verbose_name=_("file type"), choices=FileType.choices, blank=True)

    def str(self):
        return f"{self.hazard_title} - {self.hazard_type}"


class Pdc(models.Model):
    """
    Behavior from remote
    - UUID is unique
    - hazard_id doesn't change (Is this used?)
    - **hazard_type** and Others fields can change

    To view the overall information https://hazardbrief.pdc.org/PRODUCTION/ui/index.html?uuid=UUID
    Where updated_at GET params is used to retrieved snapshot data
    """

    class Status(models.TextChoices):
        ACTIVE = (
            "A",
            "Active",
        )
        EXPIRED = (
            "E",
            "Expired",
        )

    class Severity(models.TextChoices):
        WARNING = (
            "warning",
            "Warning",
        )
        WATCH = "watch", "Watch"
        ADVISORY = "advisory", "Advisory"
        INFORMATION = "information", "Information"

    stale_displacement = models.BooleanField(verbose_name=_("Requires displacement data update"), default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    # Adding following as to keep track of pdc create and update date
    pdc_created_at = models.DateTimeField(verbose_name=_("pdc created at"), null=True, blank=True)
    pdc_updated_at = models.DateTimeField(verbose_name=_("pdc updated at"), null=True, blank=True)
    hazard_id = models.CharField(verbose_name=_("hazard id"), max_length=255)
    hazard_name = models.CharField(verbose_name=_("hazard name"), max_length=255)
    hazard_type = models.CharField(max_length=100, verbose_name=_("hazard type"), choices=HazardType.choices, blank=True)
    severity = models.CharField(
        verbose_name=_("severity"),
        max_length=100,
        choices=Severity.choices,
        blank=True,
        null=True,
    )
    latitude = models.FloatField(null=True, blank=True, verbose_name=_("latitude"))
    status = models.CharField(verbose_name=_("status"), max_length=20, choices=Status.choices, blank=True)
    longitude = models.FloatField(null=True, blank=True, verbose_name=_("longitude"))
    uuid = models.UUIDField(
        verbose_name=_("uuid"),
        null=True,
        blank=True,
    )
    description = models.TextField(verbose_name=_("description"), blank=True)
    start_date = models.DateField(null=True, blank=True, verbose_name=_("start date"))
    end_date = models.DateField(null=True, blank=True, verbose_name=_("end_date"))
    footprint_geojson = models.JSONField(blank=True, null=True, default=None, verbose_name=_("Footprint Geojson"))
    storm_position_geojson = models.JSONField(blank=True, null=True, default=None, verbose_name=_("Storm Position Geojson"))
    cyclone_three_days_cou = models.JSONField(
        blank=True, null=True, default=None, verbose_name=_("Cyclone Three Days Cone of Uncertainty")
    )
    cyclone_five_days_cou = models.JSONField(
        blank=True, null=True, default=None, verbose_name=_("Cyclone Five Days Cone of Uncertainty")
    )

    def __str__(self):
        return f"{self.hazard_id} - {self.hazard_name}"


class PdcDisplacement(models.Model):
    hazard_type = models.CharField(max_length=100, verbose_name=_("hazard type"), choices=HazardType.choices, blank=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, verbose_name=_("country"), null=True, blank=True)
    pdc = models.ForeignKey(Pdc, on_delete=models.CASCADE, verbose_name=_("pdc"))
    population_exposure = models.JSONField(null=True, blank=True, default=None, verbose_name=_("population exposure"))
    capital_exposure = models.JSONField(null=True, blank=True, default=None, verbose_name=_("capital exposure"))

    def __str__(self):
        return f"{self.pdc.hazard_name} - {self.hazard_type}"


class Earthquake(models.Model):
    class MagnitudeType(models.TextChoices):
        TWO = "2", _("2")
        FOUR = "4", _("4")
        FA = "fa", _("fa")
        H = "H", _("H")
        LG = "lg", _("lg")
        M = "m", _("m")
        MA = "ma", _("ma")
        mb = "mb", _("mb")
        MBLG = "MbLg", _("MbLg")
        MB_LG = "Mb_lg", _("Mb_lg")
        MC = "mc", _("mc")
        MD = "md", _("md")
        MDL = "mdl", _("mdl")
        ME = "Me", _("Me")
        MFA = "mfa", _("mfa")
        MH = "mh", _("mh")
        MI = "Mi", _("Mi")
        MINT = "mint", _("mint")
        ML = "ml", _("ml")
        MLG = "mlg", _("mlg")
        MLR = "mlr", _("mlr")
        MLV = "mlv", _("mlv")
        MS = "Ms", _("Ms")
        MS_20 = "ms_20", _("ms_20")
        MT = "Mt", _("Mt")
        MUN = "mun", _("mun")
        MW = "mw", _("mw")
        MWB = "mwb", _("mwb")
        MWC = "mwc", _("mwc")
        MWP = "mwp", _("mwp")
        MWR = "mwr", _("mwr")
        MWW = "mwm", _("mwm")
        NO = "no", _("no")
        UK = "uk", _("uk")
        UNKNOWN = "Unknown", _("Unknown")

    event_id = models.CharField(max_length=100, verbose_name=_("event id"))
    event_title = models.CharField(max_length=255, verbose_name=_("event title"))
    event_place = models.CharField(max_length=255, verbose_name=_("event place"), null=True, blank=True)
    event_date = models.DateTimeField(verbose_name=_("event date"), null=True, blank=True)
    updated_at = models.DateTimeField(verbose_name=_("updated at"), null=True, blank=True)
    latitude = models.FloatField(verbose_name=_("latitude"))
    longitude = models.FloatField(verbose_name=_("longitude"))
    depth = models.FloatField(verbose_name=_("depth"))
    magnitude = models.FloatField(verbose_name=_("magnitude"))
    magnitude_type = models.CharField(max_length=20, choices=MagnitudeType.choices, verbose_name=_("magnitude type"))
    country = models.ForeignKey(Country, null=True, blank=True, on_delete=models.SET_NULL, verbose_name=_("country"))

    def __str__(self):
        return f"{self.event_title} - {self.magnitude}"


class Adam(models.Model):
    title = models.CharField(
        verbose_name=_("Title"),
        max_length=255,
        null=True,
        blank=True,
    )
    hazard_type = models.CharField(max_length=100, verbose_name=_("Hazard type"), choices=HazardType.choices, blank=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, verbose_name=_("Country"), null=True, blank=True)
    event_id = models.CharField(verbose_name=_("Event id"), max_length=255, null=True, blank=True)
    publish_date = models.DateTimeField(
        verbose_name=_("Publish_date"),
    )
    geojson = models.JSONField(verbose_name=_("GeJson"), null=True, blank=True)
    event_details = models.JSONField(verbose_name=_("Event Details"), null=True, blank=True)
    storm_position_geojson = models.JSONField(verbose_name=_("Storm Position"), null=True, blank=True)
    population_exposure = models.JSONField(verbose_name=_("Population Exposure"), null=True, blank=True)

    def __str__(self):
        return f"{self.title} {self.hazard_type}"


# class MeteoSwissFile(models.Model):
#     file = models.FileField(
#         blank=True, null=True,
#         verbose_name=_('Meteo File'),
#     )


class GDACS(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    # Adding following as to keep track of pdc create and update date
    start_date = models.DateTimeField(verbose_name=_("start_date"), null=True, blank=True)
    end_date = models.DateTimeField(verbose_name=_("end_date"), null=True, blank=True)
    hazard_id = models.CharField(verbose_name=_("hazard id"), max_length=255)
    episode_id = models.IntegerField(verbose_name=_("hazard episode id"), null=True, blank=True)
    hazard_name = models.CharField(verbose_name=_("hazard name"), max_length=255)
    hazard_type = models.CharField(max_length=100, verbose_name=_("hazard type"), choices=HazardType.choices, blank=True)
    alert_level = models.CharField(verbose_name=_("alert level"), null=True, blank=True, max_length=255)
    # episodeid
    country = models.ForeignKey(
        Country,
        verbose_name=_("country"),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    event_details = models.JSONField(verbose_name=_("Event Details"), null=True, blank=True)
    footprint_geojson = models.JSONField(verbose_name=_("GeJson"), null=True, blank=True)
    population_exposure = models.JSONField(verbose_name=_("Population Exposure"), null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True, verbose_name=_("latitude"))
    longitude = models.FloatField(null=True, blank=True, verbose_name=_("longitude"))

    def __str__(self):
        return f"{self.hazard_name} {self.hazard_type}"


class MeteoSwiss(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    country = models.ForeignKey(
        Country,
        verbose_name=_("country"),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    event_details = models.JSONField(verbose_name=_("Event Details"), null=True, blank=True)
    footprint_geojson = models.JSONField(verbose_name=_("GeJson"), null=True, blank=True)
    hazard_name = models.CharField(verbose_name=_("hazard name"), max_length=255)
    folder_id = models.CharField(verbose_name=_("folder id"), max_length=255)
    hazard_type = models.CharField(max_length=100, verbose_name=_("hazard type"), choices=HazardType.choices, blank=True)
    initialization_date = models.DateTimeField(verbose_name=_("initialization date"))
    event_date = models.DateTimeField(
        verbose_name=_("event date"),
    )
    impact_type = models.CharField(verbose_name=_("impact type"), max_length=255)
    model_name = models.CharField(verbose_name=_("model name"), max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.hazard_name} - {self.hazard_type}"


class MeteoSwissAgg(models.Model):
    country = models.ForeignKey(
        Country,
        verbose_name=_("country"),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    event_details = models.JSONField(verbose_name=_("Event Details"), null=True, blank=True)
    geojson_details = models.JSONField(verbose_name=_("Geojson Details"), null=True, blank=True)
    hazard_name = models.CharField(verbose_name=_("hazard name"), max_length=255)
    hazard_type = models.CharField(max_length=100, verbose_name=_("hazard type"), choices=HazardType.choices, blank=True)
    start_date = models.DateTimeField(verbose_name=_("start date"))
    updated_at = models.DateTimeField(verbose_name=_("Updated date"))
    latitude = models.FloatField(verbose_name=_("latitude"), null=True, blank=True)
    longitude = models.FloatField(verbose_name=_("longitude"), null=True, blank=True)
    model_name = models.CharField(verbose_name=_("model name"), max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.hazard_name} - {self.start_date} - {self.updated_at}"


class GWIS(models.Model):
    class DSRTYPE(models.TextChoices):
        MONTHLY = "monthly", "Monthly"
        CUMMULATIVE = "cumulative", "Cummulative"

    country = models.ForeignKey(
        Country,
        verbose_name=_("country"),
        on_delete=models.CASCADE,
    )
    month = models.CharField(verbose_name=_("month"), max_length=255)
    dsr = models.FloatField(verbose_name=_("dsr"), null=True, blank=True)
    dsr_min = models.FloatField(verbose_name=_("dsr min"), null=True, blank=True)
    dsr_avg = models.FloatField(verbose_name=_("dsr avg"), null=True, blank=True)
    dsr_max = models.FloatField(verbose_name=_("dsr max"), null=True, blank=True)
    year = models.IntegerField(
        verbose_name=_("year"),
    )
    hazard_type = models.CharField(max_length=100, verbose_name=_("hazard type"), choices=HazardType.choices, blank=True)
    dsr_type = models.CharField(max_length=100, verbose_name=_("dsr type"), choices=DSRTYPE.choices, blank=True)

    def __str__(self):
        return f"{self.country.name} - {self.year} - {self.month}"
