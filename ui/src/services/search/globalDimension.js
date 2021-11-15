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
        const response = await apiService.post("global-dimension/create/", payload)
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
        const response = await apiService.post("global-dimension/publish", payload)
        if(response.success){
            return response
        }
        else {
            message.error(response.message)
            return response
        }
    }

    async editGlobalDimension(id, payload){
        const response = await apiService.post("global-dimension/update/"+id, payload)
        if (response.success){
            return response
        }
        else{
            message.error(response.message)
            return response
        }
    }
    async deleteGlobalDimension(id){
        const response = await apiService.delete("global-dimension/delete/"+id)
        if(response.success){
            return response
        }
        else {
            message.error(response.message)
            return response
        }
    
    }

}

let globalDimensionService = new GlobalDimensionService();
export default globalDimensionService