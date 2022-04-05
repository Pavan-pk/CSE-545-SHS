import React, { useState } from 'react';
import { Form, Button, input, table } from 'react-bootstrap';
import { UserContext } from "../ContextProvider";
import HttpService from '../../Services/HttpService';
import Button1 from '@mui/material/Button';
import DeleteIcon from '@mui/icons-material/Delete';
import EditIcon from '@mui/icons-material/Delete';
import Keyboard from "react-simple-keyboard";
import "../../../node_modules/react-simple-keyboard/build/css/index.css";
import { CONFIRM_OTP, GET_DIAGNOSIS_REPORT, UPDATE_DIAGNOSIS_REPORT, USER_CONFIRM_IDENTITY_OTP, USER_SEND_OTP } from '../../Constants/PathConstants';
import { SUCCESS } from '../../Constants/StringConstant';

export default function PatientRecords(props){
    const {userid, userEmail} = React.useContext(UserContext);
    const [viewing, setViewing] = useState(false)
    const [ID, setID] = useState("")
    const [display, toggleDisplay] = useState(false)
    const [deleteEnabled, setDeleteEnable] = useState(false)
    const [askOtp, setakOtp] = useState(false)
    const [otp, setOtp] = useState("")
    const [layoutName, setLayoutName] = useState("default")
    const [textarea, setTextarea] = useState("");
    const [textarea1, setTextarea1] = useState("");
    const [textarea2, setTextarea2] = useState("");
    const [edit, setEdit] = useState(false);
    const [gotRecord, setGotRecord] = useState(false)
    
    const onKeyPress = button => {
        if (button === "{shift}" || button === "{lock}") handleShift();
      };

      const handleShift = () => {
        const ln = layoutName;
        if(ln === "default") {
            setLayoutName("shift");
        } else {
            setLayoutName("default")
        }
    };

    const verifyOtp = event =>{
        if (otp.length !== 6){
            return
        }
        const requestPayload = {"otp": otp, "email":userEmail}
        HttpService.postFetch(USER_CONFIRM_IDENTITY_OTP, requestPayload)
        .then((responseData) => {
          const response = JSON.parse(HttpService.decrypt(responseData.response))
          if(response.Status === SUCCESS){
            setEdit(true)
            setDeleteEnable(true)
          }
          else {
            props.showAlertDialog(response.Message)
          }
    })
    }

    const setAskOtp = () => {
        const requestPayload = {"email": userEmail}
        HttpService.postFetch(USER_SEND_OTP, requestPayload)
        .then((responseData) => {
          const response = JSON.parse(HttpService.decrypt(responseData.response))
          if(response.Status === SUCCESS){
            //do nothing
            setakOtp(true)
          }
          else {
            props.showAlertDialog(response.Message)
          }
    })
    }

    const getRecord = () => {
        const postJson = {
            "doctor_id": userid,
            "appointment_id": ID
        }
        HttpService.postFetch(GET_DIAGNOSIS_REPORT, postJson)
        .then((responseData) => {
          const response = JSON.parse(HttpService.decrypt(responseData.response))
          if (response.Status === SUCCESS){
              setTextarea(response.Data.diagnosis_record)
              setTextarea1(response.Data.prescription_record)
              setTextarea2(response.Data.lab_recommendation)
              setGotRecord(true)
          } else {
            props.showAlertDialog(response.Message)
          }
        })
    }

    const postDiagnosis = () => {
        const postJson = {
          "doctor_id": userid,
          "appointment_id": ID, 
          "diagnosis_record": textarea,
          "lab_recommendation": textarea2,
          "prescription_record": textarea1,
        }
        HttpService.postFetch(UPDATE_DIAGNOSIS_REPORT, postJson)
        .then((responseData) => {
          const response = JSON.parse(HttpService.decrypt(responseData.response))
          if (response.Status === SUCCESS){
            props.showAlertDialog(response.Message)
          } else {
            props.showAlertDialog(response.Message)
          }
        })
      }

    return (
        <div className="row">
            <div className="row">
                <div className="col-md-12">
                <Form.Group className="row" style={{alignItems:'center'}}>

                    <label className="col-sm-2 col-form-label">Appointment ID</label>

                    <div className="col-sm-3" style={{height:'min-content'}}>
                    <Form.Control type="numeric"  className="h-auto" maxLength={8} onChange={(event)=>setID(event.target.value)}/>
                    </div>

                    <div className="col-sm-3" style={{height:'min-content'}}>
                    <Form.Group className="row" style={{alignItems:'center', justifyContent:'space-between', paddingRight:'5rem'}}>
                    <Button className="btn col-sm-5 btn-block btn-primary font-weight-medium"
                                variant="primary"
                                type="button"
                                onClick={(e)=>getRecord()}>SUBMIT</Button>
                    </Form.Group>
                    </div>

                </Form.Group>

                </div>

            </div>

            <div className="col-lg-12 grid-margin mt-4 stretch-card">
                <div className="card">
                    <div className="card-body">
                    <h4 className="card-title">Records</h4>
                    <Form.Group className="search-field mt-1 col-md-6 mt-2">
                        <Button className="btn btn-block btn-primary col-md-6 mb-2 font-weight-medium"
                                                                                        disabled={deleteEnabled || askOtp}
                                                                                        variant="primary"
                                                                                        type="button"
                                                                                        onClick={(e) => setAskOtp(true)}>{deleteEnabled?"Modification enabled":"Enable file modifications"}</Button>
                        <div style={{display:(askOtp && !deleteEnabled ? 'block' : 'none')}}>
                            <Form.Control type="numeric" placeholder="OTP (use virtual keyboard)" size="lg" className="h-auto" maxLength={6} value={otp}/>
                                <Keyboard
                                layoutName={layoutName}
                                maxLength={6}
                                onChange={(val) => setOtp(val)}
                                onKeyPress={onKeyPress}
                                />
                                <Button className="btn btn-block btn-primary col-md-4 font-weight-medium mt-1"
                                                disabled={deleteEnabled}
                                                variant="primary"
                                                type="button"
                                                onClick={(e) => verifyOtp(e)}>
                                                    Verify OTP
                                </Button>
                        </div>
                    </Form.Group>
                    <div className="row mt-4" style={{display:gotRecord?"block":"none"}}>
                        <div className="col-md-12">
                            <Form.Group className="row form-horizontal" style={{alignItems:'center'}}>
                                <label className="col-sm-2 col-form-label">Diagnosis</label>
                                <div className="col-sm-6" style={{height:'min-content'}}>
                                <Form.Control as="textarea" disabled={!edit} value={textarea} rows={15}  className="h-auto" onChange={(event)=>setTextarea(event.target.value)}/>
                                </div>
                            </Form.Group>
                            </div>
                        </div>

                        <div className="row mt-4" style={{display:gotRecord?"block":"none"}}>
                            <div className="col-md-12">
                            <Form.Group className="row form-horizontal" style={{alignItems:'center'}}>
                                <label className="col-sm-2 col-form-label">Prescription</label>
                                <div className="col-sm-6" style={{height:'min-content'}}>
                                <Form.Control as="textarea" disabled={!edit} value={textarea1} rows={15}  className="h-auto" onChange={(event)=>setTextarea1(event.target.value)}/>
                                </div>
                            </Form.Group>
                            </div>
                        </div>

                        <div className="row mt-4" style={{display:gotRecord?"block":"none"}}>
                            <div className="col-md-12">
                            <Form.Group className="row form-horizontal" style={{alignItems:'center'}}>
                                <label className="col-sm-2 col-form-label">Lab Test</label>
                                <div className="col-sm-6" style={{height:'min-content'}}>
                                <Form.Control as="textarea" disabled={!edit} value={textarea2} rows={15}  className="h-auto" onChange={(event)=>setTextarea2(event.target.value)}/>
                                </div>
                            </Form.Group>
                            </div>
                        </div>
                        <div className="row mt-4" style={{display:edit?"block":"none"}}>
                            <Button className="btn btn-block btn-primary col-md-4 font-weight-medium mt-1"
                                                disabled={!edit}
                                                variant="primary"
                                                type="button"
                                                onClick={(e) => postDiagnosis()}>
                                                    Submit
                            </Button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    )}