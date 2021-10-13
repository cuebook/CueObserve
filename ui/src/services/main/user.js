import apiService from "./api";
import { message , notification} from "antd"

class UserService {
    login(email, password) {
        return apiService
          .post("account/login/", { email: email, password: password })
          .then(function(res) {
            if (res.success) {
              notification.success({
                message: res.message,
              });
            return res;
            }
            else {
              notification.warning({
                message: res.message
              });
              return false;
            }
          })
          .catch(error => {
            notification.warning({
              message: error.message
            });
          });
      }

      currentAccount() {
        return apiService
          .get("account/login/")
          .then(function(res) {
            if (res.success) return res;
            else {
              return res;
            }
          })
          .catch(error => {
            notification.warning({
              message: error.message
            });
          });
      }

       logout() {
        return apiService
          .delete("account/login/")
          .then(function(res) {
            if (res.success) {
                notification.success({
                  message: res.message
                })
                return true;
            }
            else return false;
          })
          .catch(error => {
            notification.error({
              message: error.message
            });
          });
      }

}

let userService = new UserService();
export default userService