import apiService from "./api";
import { message } from "antd"

class AnomalyDefService {

    async getAnomalyDefs(){
        const response = await apiService.get("anomaly/anomalyDefs")
        return response
    }
    async addAnomalyDef(payload){
        const response = await apiService.post("anomaly/addAnomalyDef" , payload)
        return response
    }
    async deleteAnomalyDef(id){
        const response = await apiService.delete("anomaly/anomalyDef/" + id)
        return response
    }

}
let anomalyDefService = new AnomalyDefService();
export default anomalyDefService;
