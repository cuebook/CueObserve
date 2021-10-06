import apiService from "./api";

class GlobalDimensionService {
    async getDimensions(){
        const response = await apiService.get("dimension/")
        return response
    }

    async AddGlobalDimension(payload){
        const response = await apiService.post("globalDimension/create/", payload)
        return response
    }

}

let globalDimensionService = new GlobalDimensionService();
export default globalDimensionService