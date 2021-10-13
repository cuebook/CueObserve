import ApiService from "services/api"

let  host = "";
let base_url = host + "/search/";

if(process.env.NODE_ENV === "development"){
  // Development Settings
 host = "http://localhost:8200";
 base_url = host + "/search/";
}
let apiService = new ApiService(base_url)
export default apiService;