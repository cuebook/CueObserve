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
    async getGlobalDimensions(){
        const response = await apiService.get("global-dimension/")
        if(response.success){
            return response.data
        }
        else {
            message.error(response.message)
            return response.data
        }
    }
    async getGlobalDimension(id){
        const response = await apiService.get("global-dimension/"+id)
        if(response.success){
            return response.data
        }
        else {
            message.error(response.message)
            return response.data
        }
    }
    async publishGlobalDimension(payload){
        const response = await apiService.post("publish/global-dimension", payload)
        if(response.success){
            return response
        }
        else {
            message.error(response.message)
            return response
        }

    }

    async editGlobalDimension(id, payload){
        const response = await apiService.post("update/global-dimension/"+id, payload)
        if (response.success){
            return response
        }
        else{
            message.error(response.message)
            return response
        }
    }


}

let globalDimensionService = new GlobalDimensionService();
export default globalDimensionService