import apiService from "./api";

class GlobalDimensionService {

    async AddGlobalDimension(payload){
        const response = await apiService.post("/global-dimension/create", payload)
        return response
    }

}

let globalDimensionService = new GlobalDimensionService();
export default globalDimensionService