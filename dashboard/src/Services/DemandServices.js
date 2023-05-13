import axios from 'axios';
import Cookies from 'js-cookie';

class DemandServices {
    getDemand(id){
        const token = Cookies.get('auth_token');
        const headers = {};
      
        if (token) {
          headers.Authorization = `Token ${token}`;
        }
       return axios.get(`http://localhost:8000/api/demand/${id}/`, {
        headers: headers,
        withCredentials: true
      });
    }
    getTransitions(id){
        const token = Cookies.get('auth_token');
        const headers = {};
      
        if (token) {
          headers.Authorization = `Token ${token}`;
        }
        return axios.get(`http://localhost:8000/api/demand/${id}/transitions/`, {
            headers: headers,
            withCredentials: true
          })
    }
    triggerTransition(id, action){
        const token = Cookies.get('auth_token');
        const headers = {};
      
        if (token) {
          headers.Authorization = `Token ${token}`;
          console.log(headers)
        }
        return axios.post(`http://localhost:8000/api/demand/${id}/${action}/`, {},{
            headers: headers,
            withCredentials: true
        })
    }
}

export default new DemandServices();