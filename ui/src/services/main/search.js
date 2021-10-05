import apiService from "./api";

class SearchService {
    async getDimensions(){
        const response = await apiService.get("anomaly/search/dimension/")
        return response
    }

    async AddGlobalDimension(payload){
        const response = await apiService.post("http://localhost:8200/search/global-dimension/create", payload)
        return response
    }

}

let searchService = new SearchService();
export default searchService