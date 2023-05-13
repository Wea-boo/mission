import axios from 'axios';
import Cookies from 'js-cookie';

class AuthServices {
    login(data){
        return axios.post("http://localhost:8000/api/login/", data, { withCredentials: true });
    }
    logout(){
        const token = Cookies.get('auth_token');
        const headers = {};
      
        if (token) {
          headers.Authorization = `Token ${token}`;
          console.log(token)
        }

        return axios.post("http://localhost:8000/api/logout/", {},{
          headers: headers,
          withCredentials: true });
        }
    checkAuth() {
        const token = Cookies.get('auth_token');
        const headers = {};
      
        if (token) {
          headers.Authorization = `Token ${token}`;
        }
      
        return axios.get("http://localhost:8000/api/check_auth/", {
          headers: headers,
          withCredentials: true
        });
      }
}

export default new AuthServices();
