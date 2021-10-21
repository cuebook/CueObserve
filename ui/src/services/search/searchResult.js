import apiService from "./api";
import {message} from "antd";

class SearchResultService {
    async getSearchCards(payload){
        const response = await apiService.post("getCards/", payload)
        if(response.success){
            return response
        }
        else{
            message.error(response.message)
            return response
        }
    }

}

let searchResultService = new SearchResultService();
export default searchResultService