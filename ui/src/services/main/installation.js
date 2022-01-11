import apiService from "./api";
import { message , notification} from "antd"

class Installation {
    async getInstallationId(){
        return  apiService.get("anomaly/installationId")
        .then(response => {
            if(response.success == true){
                return response
            } else {
                return response
            }
        })
        .catch(response => {
            return null
        })
    }
}
let installation = new Installation();
export default installation

