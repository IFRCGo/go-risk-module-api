from . import models

enum_register = {
    "gwis_dsr_type": models.GWIS.DSRTYPE,
    "earthquake_magnitude_type": models.Earthquake.MagnitudeType,
    "pdc_status": models.Pdc.Status,
    "pdc_severity": models.Pdc.Severity,
}
