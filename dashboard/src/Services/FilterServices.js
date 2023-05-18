import axios from 'axios';
import Cookies from 'js-cookie';
import API_URL from './urlConfig';


axios.defaults.baseURL = API_URL;


class FilterServices {
    getDashboardFilters() {
      const token = Cookies.get('auth_token');
      const headers = {};
  
      if (token) {
        headers.Authorization = `Token ${token}`;
      }
  
      return axios.get(`/api/dashboard-filters/`, {
        headers: headers,
        withCredentials: true,
      });
    }
  
    getFilteredDemands(creator = null, assignee = null, state = null, type = null) {
      const token = Cookies.get('auth_token');
      const headers = {};
  
      if (token) {
        headers.Authorization = `Token ${token}`;
      }

      let endpoint = `/api/demands/`;

      const params = new URLSearchParams();
      if (creator) params.append('creator', creator);
      if (assignee) params.append('assignee', assignee);
      if (state) params.append('state', state);
      if (type) params.append('_type', type);
      
      endpoint += `?${params.toString()}`;
  
      return axios.get(endpoint, {
        headers: headers,
        withCredentials: true,
      });
    }
  }
  
  export default FilterServices;