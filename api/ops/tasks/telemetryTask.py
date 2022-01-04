import logging
from celery import shared_task
from anomaly.models import  InstallationTable
from anomaly.services.telemetry import update_traits
logger = logging.getLogger(__name__)


@shared_task
def telemetryJob():
    """ Task that send telemetry at every 12:35 AM Asia/Calcutta"""
    try:
        userObj = InstallationTable.objects.all()[0]
        update_traits(userObj)
        return True
    except Exception as ex:
        return  False