import apiService from "./api";
import { message } from "antd"

class AnomalyService {
    getAnomalys(){
        return apiService.get("anomaly/anomalys")
        .then(response => {
            if(response.success == true){
                console.log(response)
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
        return apiService.get("anomaly/anomaly/" + anomalyId)
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
let anomalyService = new AnomalyService();
export default anomalyService
