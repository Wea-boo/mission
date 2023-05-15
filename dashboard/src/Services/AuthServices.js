import axios from 'axios';
import Cookies from 'js-cookie';
import API_URL from './urlConfig';

axios.defaults.baseURL = API_URL;

class AuthServices {
    login(data){
        return axios.post("/api/login/", data, { withCredentials: true });
    }
    logout(){
        const token = Cookies.get('auth_token');
        const headers = {};
      
        if (token) {
          headers.Authorization = `Token ${token}`;
          console.log(token)
        }

        return axios.post("/api/logout/", {},{
          headers: headers,
          withCredentials: true });
        }
    checkAuth() {
        const token = Cookies.get('auth_token');
        const headers = {};
      
        if (token) {
          headers.Authorization = `Token ${token}`;
        }
      
        return axios.get("/api/check_auth/", {
          headers: headers,
          withCredentials: true
        });
      }
      checkUserRoles() {
        const token = Cookies.get('auth_token');
        const headers = {};
      
        if (token) {
          headers.Authorization = `Token ${token}`;
        }
    
        return axios.get("/api/user-profile/", {
          headers: headers,
          withCredentials: true
        });
      }    
      fetchUsersInSameDirection() {
        const token = Cookies.get('auth_token');
        const headers = {};
      
        if (token) {
          headers.Authorization = `Token ${token}`;
        }
    
        return axios.get("/api/users-in-direction/", {
          headers: headers,
          withCredentials: true
        });
      }
}

export default new AuthServices();