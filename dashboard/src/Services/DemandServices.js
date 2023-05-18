import axios from 'axios';
import Cookies from 'js-cookie';
import API_URL from './urlConfig';


axios.defaults.baseURL = API_URL;

class DemandServices {
    getDemand(id){
        const token = Cookies.get('auth_token');
        const headers = {};
      
        if (token) {
          headers.Authorization = `Token ${token}`;
        }
       return axios.get(`/api/demand/${id}/`, {
        headers: headers,
        withCredentials: true
      });
    }
    postDemand( formdata, forOthers = false ){
      const endpoint = forOthers ? 'create-others-demand' : 'create-demand';
      const token = Cookies.get('auth_token');
      const headers = {};
    
      if (token) {
        headers.Authorization = `Token ${token}`;
      }
      
      return axios.post(`/api/${endpoint}/`, formdata, {
        headers: headers,
        withCredentials: true,
      });
    }
    getTransitions(id){
        const token = Cookies.get('auth_token');
        const headers = {};
      
        if (token) {
          headers.Authorization = `Token ${token}`;
        }
        return axios.get(`/api/demand/${id}/transitions/`, {
            headers: headers,
            withCredentials: true
          })
    }
    triggerTransition(id, action, validationInfo){
      action = action.replace(' ', '-');
      const token = Cookies.get('auth_token');
      const headers = {};
  
      if (token) {
        headers.Authorization = `Token ${token}`;
        console.log(headers)
      }
      
      return axios.post(`/api/demand/${id}/${action}/`, validationInfo,{
          headers: headers,
          withCredentials: true
      })
  }
}

export default new DemandServices();