import axios from "axios";
import { message } from "antd";

//create axios
//do not need baseURL: has been config in proxy
const request=axios.create({
    timeout:5000
})
// front interceptor
// get token from storage, add it to http header
request.interceptors.request.use((config) => {
    let token=localStorage.getItem("token");
    if(!!token){
        config.headers["token"]=token;
    }
    return config;
});

//back interceptor
//print out error
request.interceptors.response.use(
    (res) => {
        return res
    },
    (e) => {
        message.error(e.message);
        return Promise.reject(e);
    }
)

export default request;