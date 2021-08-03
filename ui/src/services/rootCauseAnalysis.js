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
            message.error(response.message)
            return null
        })
    }

    getAnomaly(anomalyId){
        return apiService.post("anomaly/anomaly/" + anomalyId)
        .then(response => {
            if(response.success == true){
                return response.data
            } else {
                message.error(response.message);
                return null
            }
        })
        .catch(response => {
            message.error(response.message)
            return null
        })
    }

}

let rootCauseAnalysisService = new RootCauseAnalysisService();
export default rootCauseAnalysisService
