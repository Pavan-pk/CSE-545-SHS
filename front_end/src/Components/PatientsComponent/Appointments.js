import React, { useState, useEffect } from 'react';
import { Form, Button, input, table } from 'react-bootstrap';
import { BOOK_APPOINTMENT, CANCEL_APPOINTMENT, GET_PATIENT_APPOINTMENTS } from '../../Constants/PathConstants';
import HttpService from '../../Services/HttpService';
import { UserContext } from "../ContextProvider";
import { SUCCESS } from "../../Constants/StringConstant";

export default function Appointments(props){
    const [booked, setBooked] = useState([])
    const [appointAvail, setAppointsAvail] = useState([])
    const {userid, userEmail} = React.useContext(UserContext);

    const setBookedList = (value, cancel=false, appointment_id) => {
        if (!cancel){
            const payloadJson = {
                "user_email": userEmail,
                "appointment_id": appointment_id,
                "user_id":userid
            }
            HttpService.postFetch(BOOK_APPOINTMENT, payloadJson)
            .then((responseData) => 
            {
                const response = JSON.parse(HttpService.decrypt(responseData.response))
                if (response.Status === SUCCESS){
                    setBooked([...booked,value])
                } else {
                    props.showAlertDialog(response.Message)
                }
            })
        } else {
            const payloadJson = {
                "appointment_id":appointment_id
            }
            HttpService.postFetch(CANCEL_APPOINTMENT, payloadJson)
            .then((responseData) => 
            {
                const response = JSON.parse(HttpService.decrypt(responseData.response))
                if (response.Status === SUCCESS){
                    setBooked(booked.filter(x=> x != value));
                } else {
                    props.showAlertDialog(response.Message)
                }
            })
        }
    }

    useEffect(() => {
        HttpService.postFetch(GET_PATIENT_APPOINTMENTS, {})
        .then((responseData) => 
        {
            const response = JSON.parse(HttpService.decrypt(responseData.response))
            if (response.Status === SUCCESS){
                setAppointsAvail(response.Data)
            }
        })
    },[]);

    return(
        <div className="row">
            <div className="col-lg-12 grid-margin stretch-card">
                <div className="card">
                    <div className="card-body">
                    <h4 className="card-title">Request Appointments</h4>
                    <div className="table-responsive">
                        <table className="table">
                        <thead>
                            <tr>
                            <th>Doctor</th>
                            <th>Availability</th>
                            <th>Speciality</th>
                            <th></th>
                            </tr>
                        </thead>
                        <tbody>
                            {
                                Object.entries(appointAvail).map(([key, value]) => {
                                    return (
                                    <tr>
                                        <td className="col-md-3">{value.doctor_name}</td>
                                        <td className="col-md-3">{value.time}</td>
                                        <td className="col-md-3">{value.doctor_speciality}</td>
                                        <td>
                                        {
                                            booked.includes(key) ? 
                                                <Button className="btn btn-block btn-primary col-md-6 font-weight-medium"
                                                    style={{width:"50%"}}
                                                    variant="primary"
                                                    type="button"
                                                    onClick={(e)=>setBookedList(key, true, value.appointment_id)}>Cancel</Button>
                                                    :  <Button className="btn btn-block btn-primary col-md-6 font-weight-medium"
                                                            style={{width:"50%"}}
                                                            variant="primary"
                                                            type="button"
                                                            onClick={(e)=>setBookedList(key, false, value.appointment_id)}>Request</Button>
                                        }
                                        </td>
                                    </tr>
                                    )
                                })
                            }
                        </tbody>
                        </table>
                    </div>
                    </div>
                </div>
            </div>
        </div>);
};