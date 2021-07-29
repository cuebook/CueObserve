import pytz
import logging
from django_celery_beat.models import CrontabSchedule
from anomaly.models import CustomSchedule as Schedule
from anomaly.serializers import ScheduleSerializer
from utils.apiResponse import ApiResponse


class ScheduleService:


    @staticmethod
    def getSchedules():
        """
        Service to get all schedule objects
        """
        res = ApiResponse()
        schedules = Schedule.objects.all()
        data = ScheduleSerializer(schedules, many=True).data
        res.update(True, "Schedules fetched successfully", data)
        return res
    
    @staticmethod
    def addSchedule(cron: str, timezone: str = None, name: str = ""):
        """
        Service to add Schedule
        :param cron: Crontab in string format
        :param timezone: Timezone string for which to configure Schedule
        :param name: Name of schedule provided by user
        """
        res = ApiResponse()
        cronElements = cron.split()
        if len(cronElements) != 5:
            res.update(False, "Crontab must contain five elements")
            return res        
        timezone = timezone if timezone else "UTC"
        crontabSchedule = CrontabSchedule.objects.create(
            minute=cronElements[0],
            hour=cronElements[1],
            day_of_month=cronElements[2],
            month_of_year=cronElements[3],
            day_of_week=cronElements[4],
            timezone=timezone,
        )
        schedule = Schedule.objects.create(
            name=name,
            cronSchedule=crontabSchedule
        )
        res.update(True, "Schedule added successfully", schedule.id)
        return res
        
    @staticmethod
    def getSingleSchedule(scheduleId: int):
        """
        Service to get singleSchedule
        :param scheduleId: int
        """
        res = ApiResponse()
        schedules = Schedule.objects.filter(id=scheduleId)
        data = ScheduleSerializer(schedules, many=True).data
        res.update(True, "Schedules fetched successfully", data)
        return res

    @staticmethod
    def updateSchedule(id, crontab, timezone, name):
        """
        Service to update Schedule
        param id: int
        param cron: Crontab in string format
        param timezone: Timezone in string format
        param name: String
        """
        res = ApiResponse()
        cronElements = crontab.split(" ")
        if len(cronElements) != 5:
            res.update(False, "Crontab must contain five elements")
            return res 
        schedule = Schedule.objects.get(id=id)
        schedule.cronSchedule.minute=cronElements[0]
        schedule.cronSchedule.hour=cronElements[1]
        schedule.cronSchedule.day_of_month=cronElements[2]
        schedule.cronSchedule.month_of_year=cronElements[3]
        schedule.cronSchedule.day_of_week=cronElements[4]
        schedule.cronSchedule.timezone = timezone
        schedule.cronSchedule.save()
        schedule.name = name
        schedule.save()
        res.update(True, "Schedules updated successfully", [])
        return res

    @staticmethod
    def deleteSchedule(scheduleId: int):
        """ Service to delete schedule of given scheduleId """
        res = ApiResponse()
        schedule = Schedule.objects.get(id=scheduleId)
        crontabId = schedule.cronSchedule_id
        CrontabSchedule.objects.get(id=crontabId).delete()
        schedule.delete()
        res.update(True, "Schedules deleted successfully", [])
        return res

    @staticmethod
    def getTimezones():
        """
        Service to fetch all pytz timezones
        """
        res = ApiResponse()
        timezones = pytz.all_timezones
        res.update(True, "Timezones fetched successfully", timezones)
        return res