import apiService from "./api";
import { message } from "antd"

class AnomalyDefService {

    async getAnomalyDefs(offset, limit, searchText, sorter){
        const response = await apiService.get("anomaly/anomalyDefs"+"?offset="+offset+"&limit="+limit+"&searchText="+searchText+"&sorter="+JSON.stringify(sorter))
        return response
    }
    async addAnomalyDef(payload){
        const response = await apiService.post("anomaly/addAnomalyDef" , payload)
        if(response.success == true){
            message.success(response.message)
            return response
        } else {
            message.error(response.message);
            return null
        }
    }
    async editAnomalyDef(payload){
        const response = await apiService.put("anomaly/editAnomalyDef",payload)
        if(response.success == true){
            message.success(response.message)
            return response
        } else {
            message.error(response.message);
            return null
        }
    }
    async deleteAnomalyDef(id){
        const response = await apiService.delete("anomaly/anomalyDef/" + id)
        if(response.success == true){
            message.success(response.message)
            return response
        } else {
            message.error(response.message);
            return null
        }
    }
    async runAnomalyDef(id){
        const response = await apiService.post("anomaly/runAnomalyDef/" + id)
        if(response.success == true){
            message.success(response.message)
            return response
        } else {
            message.error(response.message);
            return null
        }
    }
    async getDetectionRuns(anomalyDefId, offset){
        const response = await apiService.get("anomaly/runStatus/" + anomalyDefId + "?offset=" + offset)
        if(response.success == true)
            return response.data
        else
            return null
    }
    async isTaskRunning(anomalyDefId){
        const response = await apiService.get("anomaly/isTaskRunning/" + anomalyDefId)
        if(response.success == true)
            return response.data
        else
            return null
    }
    async getRunStatusAnomalies(runStatusId){
        const response = await apiService.get("anomaly/runStatusAnomalies/" + runStatusId)
        if(response.success == true)
            return response.data
        else
            return null
    }

}
let anomalyDefService = new AnomalyDefService();
export default anomalyDefService;
