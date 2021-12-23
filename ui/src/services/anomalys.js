import apiService from "./api";
import { message } from "antd"

class AnomalyService {
    getAnomalys(publishedOnly, offset, limit, searchText, sorter){
        let url = publishedOnly ? "anomaly/anomalys" : "anomaly/allanomalys"
        return apiService.get(url + "?offset="+offset+ "&limit="+limit +"&searchText="+searchText + "&sorter="+ JSON.stringify(sorter))
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
            // message.error(response.message)
            return null
        })
    }

}
let anomalyService = new AnomalyService();
export default anomalyService
