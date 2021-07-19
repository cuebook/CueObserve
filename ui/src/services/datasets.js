import apiService from "./api";
import { message } from "antd"

class DatasetService {
    getDatasets(){
        return apiService.get("anomaly/datasets")
        .then(response => {
            if(response.success == true){
                return response.data
            } else {
                message.error(response.message);
                return null
            }
        })
        .catch(response => {
            message.error(response.message)
            return null
        })
    }

    getDataset(datasetId){
        return apiService.get("anomaly/dataset/" + datasetId)
        .then(response => {
            if(response.success == true){
                return response.data
            } else {
                message.error(response.message);
                return null
            }
        })
        .catch(response => {
            message.error(response.message)
            return null
        })
    }

    updateDataset(datasetId, payload){
        return apiService.post("anomaly/dataset/" + datasetId, payload)
        .then(response => {
            if(response.success == true){
                message.success(response.message)
                return response.data
            } else {
                message.error(response.message);
                return null
            }
        })
        .catch(response => {
            message.error(response.message)
            return null
        })
    }

    deleteDataset(datasetId){
        return apiService.delete("anomaly/dataset/" + datasetId)
        .then(response => {
            if(response.success == true){
                message.success(response.message)
                return true
            } else {
                message.error(response.message);
                return null
            }
        })
        .catch(response => {
            message.error(response.message)
            return null
        })
    }

    createDataset(payload){
        return apiService.post("anomaly/dataset/create", payload)
        .then(response => {
            if(response.success == true){
                message.success(response.message)
                return true
            } else {
                message.error(response.message);
                return null
            }
        })
        .catch(response => {
            message.error(response.message)
            return null
        })
    }

    runSQL(payload){
        return apiService.post("anomaly/dataset/run", payload)
        .then(response => {
            if(response.success == true){
                return response.data
            } else {
                message.error(response.message);
                return null
            }
        })
        .catch(response => {
            message.error(response.message)
            return null
        })
    }

}
let datasetService = new DatasetService();
export default datasetService
