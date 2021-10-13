
import apiService from "./api";
import { message } from "antd"

class ScheduleService{

    async getSchedules(){
        const response = await apiService.get("anomaly/schedules/")
        if(response.success == true)
            return response.data
        else    
            return null
    }

    async deleteSchedule(scheduleId){
        const response = await apiService.delete("anomaly/schedules/" + scheduleId)
        if(response.success == true)
            return response
        else    
            return null
    }
    

    async getSingleSchedule(scheduleId){
        const response = await apiService.get("anomaly/schedules/" + scheduleId)
        if(response.success == true)
            return response.data
        else    
            return null
    }


    async getTimezones(){
        const response = await apiService.get("anomaly/timezones/")
        if(response.success == true)
            return response.data
        else 
            return null
    }

    async addSchedule(cronTabSchedule, selectedTimezone, scheduleName){
        const response = await apiService.post("anomaly/schedules/", {"crontab": cronTabSchedule, "timezone": selectedTimezone, "name": scheduleName})
        return response
    }

    async updateSchedule(selectedScheduleId,cronTabSchedule, selectedTimezone, scheduleName){
        const response = await apiService.put("anomaly/schedules/", {"id":selectedScheduleId,"crontab": cronTabSchedule, "timezone": selectedTimezone, "name": scheduleName})
        return response
    }

    async addAnomalyDefSchedule(anomalyDefId, scheduleId){
        const response = await apiService.post("anomaly/anomalyDefJob/", {anomalyDefId: anomalyDefId,scheduleId: scheduleId})
        return response
    }

    async unassignSchedule(anomalyDefId){
        const response = await apiService.delete("anomaly/anomalyDefJob/" + anomalyDefId)
        return response
    }

}

let scheduleService = new ScheduleService();
export default scheduleService;