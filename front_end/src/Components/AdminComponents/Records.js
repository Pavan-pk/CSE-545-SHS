import React, { useState } from 'react';
import { Form, Button } from 'react-bootstrap';
import HttpService from '../../Services/HttpService';
import Keyboard from "react-simple-keyboard";
import "../../../node_modules/react-simple-keyboard/build/css/index.css";
import { DELETE_USER_RECORD, GET_DIAGNOSIS_REPORT, USER_CONFIRM_IDENTITY_OTP, USER_SEND_OTP } from '../../Constants/PathConstants';
import { SUCCESS } from '../../Constants/StringConstant';
import { UserContext } from "../ContextProvider";

export default function Records(props){
    const {userid, userEmail} = React.useContext(UserContext);
    const [ID, setID] = useState("")
    const [deleteEnabled, setDeleteEnable] = useState(false)
    const [askOtp, setakOtp] = useState(false)
    const [otp, setOtp] = useState("")
    const [layoutName, setLayoutName] = useState("default")
    
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

    const deleteRecord = () => {
        const postJson = {
            "user_id": ID
        }
        HttpService.postFetch(DELETE_USER_RECORD, postJson)
        .then((responseData) => {
          const response = JSON.parse(HttpService.decrypt(responseData.response))
          props.showAlertDialog(response.Message)
          setID("")
        })
    }

    return (
        <div className="row">
            <div className="row">
                <div className="col-lg-12 grid-margin mt-4 stretch-card">
                    <div className="card">
                        <div className="card-body">
                            <h4 className="card-title">Records</h4>
                            <div className="col-md-12">
                                    <Form.Group className="search-field mt-1 col-md-6 mt-2">
                                        <Button className="btn btn-block btn-primary col-md-6 mb-2 font-weight-medium"
                                                                                                        disabled={deleteEnabled || askOtp}
                                                                                                        variant="primary"
                                                                                                        type="button"
                                                                                                        onClick={(e) => setAskOtp(true)}>{deleteEnabled?"Delete enabled":"Enable delete operations"}</Button>
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
                                    <Form.Group className="row" style={{alignItems:'center', display: deleteEnabled?"block":"none"}}>
                                        <label className="col-sm-2 pl-3 col-form-label">User ID</label>
                                        <div className="col-sm-3" style={{height:'min-content'}}>
                                            <Form.Control type="numeric"  className="h-auto" maxLength={8} value={ID} onChange={(event)=>setID(event.target.value)}/>
                                        </div>

                                        <div className="col-sm-4 mt-2" style={{height:'min-content', marginLeft:"0.75rem"}}>
                                            <Form.Group className="row" style={{alignItems:'center', justifyContent:'space-between', paddingRight:'5rem'}}>
                                            <Button className="btn col-sm-5 btn-block btn-primary font-weight-medium"
                                                        variant="primary"
                                                        type="button"
                                                        onClick={(e)=>deleteRecord()}>SUBMIT</Button>
                                            </Form.Group>
                                        </div>
                                    </Form.Group>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    )}