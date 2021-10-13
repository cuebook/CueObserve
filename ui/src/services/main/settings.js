import apiService from "./api";
import { message } from "antd"

class SettingService {
    getSettings(){
        return apiService.get("anomaly/settings")
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

    updateSettings(payload){
        return apiService.post("anomaly/settings", payload)
        .then(response => {
            if(response.success == true){
                return true
            } else {
                message.error(response.message);
                return false
            }
        })
        .catch(response => {
            message.error(response.message)
            return null
        })
    }
}

let settingService = new SettingService();
export default settingService
