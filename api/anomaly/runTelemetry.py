import random
import string
import os
import logging
from django_celery_beat.models import PeriodicTask, CrontabSchedule
from anomaly.models import InstallationTable
from anomaly.services.telemetry import update_traits, getInstallationId
from ops.tasks.telemetryTask import telemetryJob

logger = logging.getLogger(__name__)



def create_installation_userId():
    """ Create a random user while installation """
    try:
        res = getInstallationId()
        userId = res.data.get("installationId", "UnIdentified")
        update_traits()
        # job creation
        create_celery_job(userId)

    except Exception as ex:
        logger.error("Exception occured while creating installtion userId %s", str(ex))


    
def create_celery_job(userId):
    """ Create a celery job only once while installation"""
    try:
        crontab = "15 1 * * *"
        cronElements = crontab.split(" ")
        cronSchedule = CrontabSchedule.objects.create()
        cronSchedule.minute=cronElements[0]
        cronSchedule.hour=cronElements[1]
        cronSchedule.day_of_month=cronElements[2]
        cronSchedule.month_of_year=cronElements[3]
        cronSchedule.day_of_week=cronElements[4]
        cronSchedule.save()
        ptask = PeriodicTask.objects.update_or_create(name = "UserTelemetry" ,defaults={"crontab" : cronSchedule, "task" : telemetryJob.name})
    except Exception as ex:
        logger.error("Exception occured while creating celery job %s",str(ex))
