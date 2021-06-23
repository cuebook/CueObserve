import apiService from "./api";
import { store } from 'react-notifications-component';

class AnomalyService {
    async getAnomalys(){
        const response = await apiService.get("anomaly/anomalys")
        if(response.success == true)
            return response.data
        else
            return null
    }
}
let anomalyService = new AnomalyService();
export default anomalyService
