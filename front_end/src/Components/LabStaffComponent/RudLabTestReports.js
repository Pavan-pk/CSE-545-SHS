import React, { useState, useEffect } from 'react';
import { Form, Button, input, table } from 'react-bootstrap';
import "../../../node_modules/react-simple-keyboard/build/css/index.css";
import { DELETE_LAB_REPORT, GET_LAB_TEST_REPORTS } from '../../Constants/PathConstants';
import HttpService from "../../Services/HttpService"
import { SUCCESS } from '../../Constants/StringConstant';

export default function RudLabTestReports(props){
    const [labRecord, setLabRcord] = useState([])

    useEffect(() => {
        getLabTestRequests()
    }, []);

    const getLabTestRequests = () => {
        HttpService.postFetch(GET_LAB_TEST_REPORTS, {})
        .then((responseData) => {
          const response = JSON.parse(HttpService.decrypt(responseData.response))
          if (response.Status === SUCCESS){
            setLabRcord(response.Data)
          } else {
            props.showAlertDialog(response.Message)
          }
        })
    }

    const deleteData = (value) => {
        const payloadJson = {"lab_id": value.lab_id}
        HttpService.postFetch(DELETE_LAB_REPORT, payloadJson)
        .then((responseData) => {
            const response = JSON.parse(HttpService.decrypt(responseData.response))
            if (response.Status === SUCCESS){
              props.showAlertDialog(response.Message)
              getLabTestRequests()
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
                    <h4 className="card-title">Lab Records</h4>
                    {
                        labRecord.length === 0  ?
                        <p className="card-description"> No records to show. </p> :
                            (
                                <div>  
                                    {
                                        labRecord.length !== 0 && (
                                            <div style={{marginTop:"3rem"}}>
                                                <div className='table-responsive'>
                                                    <table className='table'>
                                                        <thead>
                                                            <tr>
                                                                <th>Appointment ID</th>
                                                                <th>User ID</th>
                                                                <th>Lab recommendation</th>
                                                                <th>Lab report</th>
                                                                <th>Status</th>
                                                                <th></th>
                                                            </tr>
                                                        </thead>
                                                        <tbody>
                                                            {
                                                                Object.entries(labRecord).map(([key,value]) => {
                                                                    return (
                                                                        <tr>
                                                                            <td className="col-md-1">{value.appointment_id}</td>
                                                                            <td className="col-md-1">{value.user_id}</td>
                                                                            <td className="col-md-2" >{value.lab_recommendation}</td>
                                                                            <td className='col-md-4'>{value.lab_report}</td>
                                                                            <td className='col-md-1'>{value.status}</td>
                                                                            <td className="col-md-1">
                                                                                <Button className="btn btn-block btn-primary col-md-12 font-weight-medium"
                                                                                    variant="primary"
                                                                                    type="button"
                                                                                    onClick={(e)=>deleteData(value)}>Delete</Button>
                                                                            </td> 
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