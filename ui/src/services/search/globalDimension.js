import apiService from "./api";

class GlobalDimensionService {

    async AddGlobalDimension(payload){
        const response = await apiService.post("globalDimension/create/", payload)
        return response
    }

}

let globalDimensionService = new GlobalDimensionService();
export default globalDimensionService