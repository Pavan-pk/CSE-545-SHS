import React, { useState, useEffect } from 'react';
import { Form, Button, input, table } from 'react-bootstrap';
import { UserContext } from "../ContextProvider";
import Button1 from '@mui/material/Button';
import { DropdownButton } from 'react-bootstrap';
import { Dropdown } from 'react-bootstrap';
import DeleteIcon from '@mui/icons-material/Delete';
import EditIcon from '@mui/icons-material/Delete';
import Keyboard from "react-simple-keyboard";
import "../../../node_modules/react-simple-keyboard/build/css/index.css";
import HttpService from '../../Services/HttpService';
import {APPROVE_APPOINTMENTS, GET_APPOINTMENT_REQUESTS, REJECT_APPOINTMENTS} from "../../Constants/PathConstants";
import {SUCCESS} from "../../Constants/StringConstant"

export default function ApproveAppointment(props){
    const [appointmentList, setAppointmentList] = useState([])

    useEffect(()=> {
        setAppointmentLists()
    }, [])

    const setAppointmentLists = () => {
        HttpService.postFetch(GET_APPOINTMENT_REQUESTS, {})
        .then((responseData) => 
        {
            const response = JSON.parse(HttpService.decrypt(responseData.response))
            if (response.Status === SUCCESS){
                setAppointmentList(response.Data.Data)
              } else {
                props.showAlertDialog(response.Message)
              }
        })
    }
    const approveData = (postJson) => {
        HttpService.postFetch(APPROVE_APPOINTMENTS, postJson)
        .then((responseData) => {
            const response = JSON.parse(HttpService.decrypt(responseData.response))
            if (response.Status === SUCCESS){
                setAppointmentLists()
              } else {
                props.showAlertDialog(response.Message)
            }
        })
    }

    const rejectData = (postJson) => {
        HttpService.postFetch(REJECT_APPOINTMENTS, postJson)
        .then((responseData) => {
            const response = JSON.parse(HttpService.decrypt(responseData.response))
            if (response.Status === SUCCESS){
                setAppointmentLists()
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
                    <h4 className="card-title">Appointments</h4>
                    {
                        appointmentList.length === 0  ?
                        <p className="card-description"> No appointments to approve. </p> :
                            (
                                <div>  
                                    {
                                        appointmentList.length !== 0 && (
                                            <div style={{marginTop:"3rem"}}>
                                              
                                                <div className='table-responsive'>
                                                    <table className='table'>
                                                        <thead>
                                                            <tr>
                                                                <th>Appointment #</th>
                                                                <th>Doctor</th>
                                                                <th>Time</th>
                                                                <th></th>
                                                                <th></th>
                                                            </tr>
                                                        </thead>
                                                        <tbody>
                                                            {
                                                                Object.entries(appointmentList).map(([key,value]) => {
                                                                    return (
                                                                        <tr>
                                                                            <td className="col-md-2">{value.appointment_id}</td>
                                                                            <td className="col-md-3">{value.doctor_name}</td>
                                                                            <td className="col-md-3">{value.time}</td>
                                                                            <td className="col-md-1">
                                                                                <Button className="btn btn-block btn-primary col-md-12 font-weight-medium"
                                                                                    variant="primary"
                                                                                    type="button"
                                                                                    onClick={(e)=>approveData({"appointment_id": value.appointment_id, 
                                                                                                                "user_email":value.user_email,
                                                                                                                "user_id":value.user_id,
                                                                                                                "doctor_name":value.doctor_name,
                                                                                                                "time":value.time})}>Approve</Button>
                                                                            </td>
                                                                            <td className="col-md-1">
                                                                                <Button className="btn btn-block btn-primary col-md-12 font-weight-medium"
                                                                                    variant="primary"
                                                                                    type="button"
                                                                                    onClick={(e)=>rejectData({"appointment_id": value.appointment_id, 
                                                                                                                "user_email":value.user_email,
                                                                                                                "user_id":value.user_id,
                                                                                                                "doctor_name":value.doctor_name,
                                                                                                                "time":value.time})}>Reject</Button>
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