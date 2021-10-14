import apiService from "./api";
import {message} from "antd";

class GlobalDimensionService {
    async getDimensions(){
        const response = await apiService.get("dimension/")
        if(response.success){
            return response.data
        }
        else{
            message.error(response.message)
            return response.data
        }
    }

    async AddGlobalDimension(payload){
        const response = await apiService.post("globalDimension/create/", payload)
        if(response.success){
            return response
        }
        else{
            message.error(response.message)
            return response
        }
    }
    async getGlobalDimension(){
        const response = await apiService.get("global-dimension/")
        if(response.success){
            return response.data
        }
        else {
            message.error(response.message)
            return response.data
        }
    }

}

let globalDimensionService = new GlobalDimensionService();
export default globalDimensionService