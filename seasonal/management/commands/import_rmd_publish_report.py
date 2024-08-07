import logging

import requests
from django.core.management.base import BaseCommand

from common.models import Country
from common.utils import logging_response_context
from seasonal.models import PublishReport, PublishReportProgram

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Import RMD Publish Data"

    def handle(self, *args, **options):
        rmd_url = "https://rmd-api-prod-appservice.azurewebsites.net/publishreport"
        response = requests.get(rmd_url)
        if response.status_code != 200:
            logger.error(
                "Error querying ipc data",
                extra=logging_response_context(response),
            )
        rmd_data = response.json()
        for program_data in rmd_data:
            if Country.objects.filter(name__icontains=program_data["program"]["country"]).exists():
                # create pulish report program
                data = {
                    "start_date": program_data["program"]["startDate"],
                    "end_date": program_data["program"]["endDate"],
                    "inactive": program_data["program"]["inactive"],
                    "country": Country.objects.filter(name__icontains=program_data["program"]["country"]).first(),
                    "program_name": program_data["program"]["programName"],
                    "area": program_data["program"]["area"],
                    "description": program_data["program"]["description"],
                    "communities": program_data["program"]["communities"],
                    "bread_cumbs": program_data["program"]["breadCrumbs"],
                    "accuracy_level": program_data["program"]["accuracyLevel"],
                    "community_engagement": program_data["program"]["communityEngagement"],
                    "measurement_assignment": program_data["program"]["measurementAssignment"],
                    "community_vca": program_data["program"]["communityeVCA"],
                }
                program = PublishReportProgram.objects.create(**data)
                # create publish report
                report_data = {
                    "program": program,
                    "report_name": program_data["reportName"],
                    "description": program_data["description"],
                    "email": program_data["email"],
                    "attachment_name": program_data["attachmentName"],
                    "attachment": program_data["attachment"],
                    "publish_report_id": program_data["id"],
                }
                report = PublishReport.objects.create(**report_data)
                if report.attachment_name:
                    report.attachment_url = f"https://rmd-api.ifrc.org/publishreport/download/{report.publish_report_id}"
                    report.save(update_fields=["attachment_url"])
