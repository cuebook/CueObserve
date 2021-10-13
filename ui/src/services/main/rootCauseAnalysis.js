import apiService from "./api";
import { message } from "antd"

class RootCauseAnalysisService {
    getRCA(anomalyId){
        return apiService.get("anomaly/rca/"+anomalyId)
        .then(response => {
            if(response.success == true){
                return response.data
            } else {
                message.error(response.message);
                return null
            }
        })
        .catch(response => {
            return null
        })
    }

    doRCA(anomalyId){
        return apiService.post("anomaly/rca/" + anomalyId)
        .then(response => {
            if(response.success == true){
                return true
            } else {
                message.error(response.message);
                return null
            }
        })
        .catch(response => {
            return null
        })
    }

    abortRCA(anomalyId){
        return apiService.delete("anomaly/rca/" + anomalyId)
        .then(response => {
            if(response.success == true){
                return true
            } else {
                message.error(response.message);
                return null
            }
        })
        .catch(response => {
            return null
        })
    }

}

let rootCauseAnalysisService = new RootCauseAnalysisService();
export default rootCauseAnalysisService
