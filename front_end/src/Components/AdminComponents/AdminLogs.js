import React, { useState, useEffect } from 'react';
import "../../../node_modules/react-simple-keyboard/build/css/index.css";
import HttpService from '../../Services/HttpService';
import {GET_OPERATION_LOGS} from "../../Constants/PathConstants";
import {SUCCESS} from "../../Constants/StringConstant"

export default function AdminLogs(props){
    const [logs, setLogs] = useState([])

    useEffect(()=> {
        getlogs()
    }, [])

    const getlogs = () => {
        HttpService.postFetch(GET_OPERATION_LOGS, {})
        .then((responseData) => 
        {
            const response = JSON.parse(HttpService.decrypt(responseData.response))
            if (response.Status === SUCCESS){
                if(!!response.Data){
                    setLogs(response.Data)
                } else {
                    setLogs([])
                }
              } else {
                props.showAlertDialog(response.Message)
              }
        })
    }

    return(

        <div className="row">

            <div className="col-lg-12 grid-margin mt-4 stretch-card" >
                <div className="card">
                    <div className="card-body">
                    <h4 className="card-title">Logs</h4>
                    {
                        logs.length === 0  ?
                        <p className="card-description"> No log record </p> :
                            (
                                <div>  
                                    {
                                        logs.length !== 0 && (
                                            <div style={{marginTop:"3rem"}}>
                                              
                                                <div className='table-responsive'>
                                                    <table className='table'>
                                                        <thead>
                                                            <tr>
                                                                <th>Log ID</th>
                                                                <th>Time</th>
                                                                <th>Message</th>
                                                            </tr>
                                                        </thead>
                                                        <tbody>
                                                            {
                                                                Object.entries(logs).map(([key,value]) => {
                                                                    return (
                                                                        <tr>
                                                                            <td className="col-md-2">{value.log_record_id}</td>
                                                                            <td className="col-md-3">{value.time}</td>
                                                                            <td className="col-md-3" style={{wordWrap:"break-word"}}>{value.message}</td>
                                                                        </tr>
                                                                    )
                                                                })
                                                            }
                                                        </tbody>
                                                    </table>
                                                </div>
                                            </div>
                                        )
                                    }
                                </div>  
                            )
                        }
                    </div>
                </div>
            </div>
        </div>);
};