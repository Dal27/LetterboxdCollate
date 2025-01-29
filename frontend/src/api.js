import axios from 'axios';

//Create an axios instance
const api = axios.create({
    baseURL: 'http://localhost:8000',
    timeout: 500000,
});

//Export the instance
export default api;