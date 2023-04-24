import axios from 'axios';

class AuthServices {
    login(data){
        return axios.post("http://localhost:8000/api/login/", data, { withCredentials: true });
    }
    logout(){
        return axios.post("http://localhost:8000/api/logout/", { withCredentials: true });
    }
    checkAuth() {
        return axios.get("http://localhost:8000/api/check_auth/", { withCredentials: true });
    }
}

export default new AuthServices();
