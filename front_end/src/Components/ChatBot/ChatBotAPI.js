import HttpService from "../../Services/HttpService";
import {GET_CHATBOT_REPLY} from "../../Constants/PathConstants";
import { SUCCESS } from "../../Constants/StringConstant";

const API = {
    GetChatbotResponse: async (usertype, message) => {
      return new Promise(function(resolve, reject) {
        setTimeout(function() {
          if (message === "hi") resolve("Welcome to chatbot!");
          else {
            const requestPayload = {
              "user_type":usertype,
              "query":message,
            }
            HttpService.postFetch(GET_CHATBOT_REPLY, requestPayload)
            .then((responseData) => {
              const response = JSON.parse(HttpService.decrypt(responseData.response))
              if(response.Status == SUCCESS){
                resolve(response.Data)
              } else {
                resolve(response.Message)
              }
            })
          }
        }, 2000);
      });
    }
  };
  
  export default API;
  