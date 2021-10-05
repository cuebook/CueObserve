import ApiService from "services/api"

let host = "";
let base_url = host + "/api/";

if(process.env.NODE_ENV === "development"){
  // Development Settings
 host = "http://localhost:8000";
 base_url = host + "/api/";
}

let apiService = new ApiService(base_url)
export default apiService;