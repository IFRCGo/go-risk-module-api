import logging

from django.core.management.base import BaseCommand

from seasonal.models import InformRisk, InformRiskSeasonal


logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Update inform annual seasonal data"

    def handle(self, *args, **kwargs):
        inform_risk = InformRisk.objects.all()
        for risk in inform_risk:
            risk_seasonal = InformRiskSeasonal.objects.filter(
                country=risk.country,
                hazard_type=risk.hazard_type
            )
            if risk_seasonal.exists():
                risk_seasonal = risk_seasonal.first()
                risk_seasonal.annual_average = risk.risk_score
                risk_seasonal.save(update_fields=['annual_average'])
