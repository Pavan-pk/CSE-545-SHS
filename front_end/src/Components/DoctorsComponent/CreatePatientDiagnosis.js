import React, {useEffect, useState}  from 'react';
import { Form, Button } from 'react-bootstrap';
import HttpService from '../../Services/HttpService';
import { UserContext } from "../ContextProvider";
import {GET_APPOINTMENT_DATA, CREATE_DIAGNOSIS_REPORT} from "../../Constants/PathConstants"
import { SUCCESS } from '../../Constants/StringConstant';

export default function CreatePatientDiagnosis(props) {
  const {userid, } = React.useContext(UserContext);
  const [ID, setID] = useState("")
  const [textarea, setTextarea] = useState("");
  const [textarea1, setTextarea1] = useState("");
  const [textarea2, setTextarea2] = useState("");
  const [edit, setEdit] = useState(false);
  const [appointmentId, setAppointmentId] = useState("")
  const [submit, setSubmit] = useState(false)
  const [userObj, setUserObj] = useState({})
  
  const populate = (userData) =>{
    setAppointmentId(userData.appointment_id)
    setUserObj(userData)
  }

  const postDiagnosis = () => {
    const postJson = {
      "user_id": userObj.user_id,
      "user_email": userObj.user_email,
      "doctor_id": userid,
      "doctor_name": userObj.doctor_name,
      "doctor_email": userObj.doctor_email,
      "diagnosis_record": textarea,
      "lab_recommendation": textarea2,
      "prescription_record": textarea1,
      "appointment_id": appointmentId, 
    }
    HttpService.postFetch(CREATE_DIAGNOSIS_REPORT, postJson)
    .then((responseData) => {
      const response = JSON.parse(HttpService.decrypt(responseData.response))
      if (response.Status === SUCCESS){
        props.showAlertDialog(response.Message)
      } else {
        props.showAlertDialog(response.Message)
      }
    })
  }
  const getAppointments = () => {
    const postJson = {"doctor_id": userid}
    HttpService.postFetch(GET_APPOINTMENT_DATA, postJson)
    .then((responseData) => {
      const response = JSON.parse(HttpService.decrypt(responseData.response))
      if (response.Status === SUCCESS){
        populate(response.Data)
        setEdit(true)
        setSubmit(true)
        props.showAlertDialog(response.Message)
      } else {
        props.showAlertDialog(response.Message)
        setEdit(false)
      }
    })
  }
  
  const handleSubmit = (event) => {
    event.preventDefault(); 
    postDiagnosis();
    setEdit(false)
    setSubmit(false)
  }

return (


<div>
<div className="row">
  <div className="col-12 grid-margin">
    <div className="card">
      <div className="card-body">
        <form className="form-sample">
        <div className="row">
            <div className="col-md-12">
              <Form.Group className="row" style={{alignItems:'center', justifyContent:'space-between', paddingRight:'5rem'}}>
                <Button className="btn col-sm-3 mb-2 btn-block btn-primary font-weight-medium"
                        variant="primary"
                        type="button"
                        onClick={(e)=>getAppointments()}>Get appointment details</Button>
              </Form.Group>
            </div>
          </div>
          <div className="row">
            <div className="col-md-12">
              <Form.Group className="row" style={{alignItems:'center'}}>
                <label className="col-sm-2 col-form-label">Appointment ID</label>
                <div className="col-sm-3" style={{height:'min-content'}}>
                  <Form.Control type="text" disabled  className="h-auto" value={appointmentId} onChange={(event)=>setID(event.target.value)}/>
                </div>
              </Form.Group>
            </div>
          </div>

          <div className="row mt-4">
            <div className="col-md-12">
              <Form.Group className="row form-horizontal" style={{alignItems:'center'}}>
                <label className="col-sm-2 col-form-label">Diagnosis</label>
                <div className="col-sm-6" style={{height:'min-content'}}>
                <Form.Control as="textarea" disabled={!edit} value={textarea} rows={15}  className="h-auto" onChange={(event)=>setTextarea(event.target.value)}/>
                </div>
              </Form.Group>
            </div>
          </div>

          <div className="row mt-4">
            <div className="col-md-12">
              <Form.Group className="row form-horizontal" style={{alignItems:'center'}}>
                <label className="col-sm-2 col-form-label">Prescription</label>
                <div className="col-sm-6" style={{height:'min-content'}}>
                <Form.Control as="textarea" disabled={!edit} value={textarea1} rows={15}  className="h-auto" onChange={(event)=>setTextarea1(event.target.value)}/>
                </div>
              </Form.Group>
            </div>
          </div>

          <div className="row mt-4">
            <div className="col-md-12">
              <Form.Group className="row form-horizontal" style={{alignItems:'center'}}>
                <label className="col-sm-2 col-form-label">Lab Test</label>
                <div className="col-sm-6" style={{height:'min-content'}}>
                <Form.Control as="textarea" disabled={!edit} value={textarea2} rows={15}  className="h-auto" onChange={(event)=>setTextarea2(event.target.value)}/>
                </div>
              </Form.Group>
            </div>
          </div>
         
          <div>
            <div className="row mt-5 col-sm-2 d-flex flex-column">
            <Button className="btn btn-block btn-primary btn-lg font-weight-medium auth-form-btn" disabled={!edit} variant="primary" onClick={handleSubmit} type="submit">{"SUBMIT"}</Button>
            </div>
          </div>

        </form>
      </div>
    </div>
  </div>
</div>
</div>

  )
}