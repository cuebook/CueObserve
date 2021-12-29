import random
import string
import os
from django_celery_beat.models import PeriodicTask, CrontabSchedule
from anomaly.services.telemetry import update_traits
from ops.tasks.telemetryTask import telemetryJob

def create_installation_userId():
    """ Create a random user while installation """

    from anomaly.models import InstallationTable
    userId = ''.join(random.choices(string.ascii_uppercase + string.digits, k=16))

    if not InstallationTable.objects.all().exists():
        userId = ''.join(random.choices(string.ascii_uppercase + string.digits, k=16))
        dbType = ""
        if os.environ.get("POSTGRES_DB_HOST", False):
            dbType = "postgres"
        else:
            dbType = "sqlite"
        userObj = InstallationTable.objects.create(installationId = userId, databaseType = dbType)
        update_traits(userObj)
        # job creation
        create_celety_job(userId)
    
def create_celety_job(userId):
    """ Create a celery job only once while installation"""

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


create_installation_userId()