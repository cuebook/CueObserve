import apiService from "./api";
import { message , notification} from "antd"

class Installation {
    async getInstallationId(){
        const response = await apiService.get("anomaly/installationId")
        return response
    }
}
let installation = new Installation();
export default installation

