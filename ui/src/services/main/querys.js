import apiService from "./api";
import { message } from "antd"

class QueryService {
    runQuery(payload){
        return apiService.post("anomaly/runQuery", payload)
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

let queryService = new QueryService();
export default queryService
