import React, { Component, useEffect, useState } from 'react';
import { Form, Button, Alert } from 'react-bootstrap';
import icon from '../assets/images/icon.png'
import { useNavigate , Link} from "react-router-dom";
import HttpService from "../Services/HttpService";
import Keyboard from "react-simple-keyboard";
import "../../node_modules/react-simple-keyboard/build/css/index.css";
import { SEND_OTP_WITHOUT_TOKEN, USER_CONFIRM_IDENTITY_OTP, USER_FORGOT_PASSWORD } from '../Constants/PathConstants';
import {SUCCESS, FAILURE} from "../Constants/StringConstant";

export default function PasswordReset() {
    const [email, setEmail] = useState("")
    const [password, setPassword] = useState("")
    const [verifyPassword, setVerifyPassword] = useState("")
    // States 0 -> ask email, 1 -> ask otp, 2 -> password
    const [currState, setCurrState] = useState(0)
    const [otp, setOtp] = useState("")
    const [userType, setUserType] = useState('0')
    const navigate = useNavigate(); 
    const [layoutName, setLayoutName] = useState("default")
    const [showAlert, setShowAlert] = useState(false)
    const [alertMsg, setAlertMsg] = useState('')
    const showAlertDialog = (msg) => {
      setAlertMsg(msg)
      setShowAlert(true)
      setTimeout(()=>setShowAlert(false), 3000)
    }
    
    const handleSubmit = (event) => {
      event.preventDefault();
      switch(currState){
          case 0:
            if (email === '' || userType === '0') return;
            const postPayload0 = {"email": email, 'user_type': userType}
            HttpService.postFetch(SEND_OTP_WITHOUT_TOKEN, postPayload0)
            .then((responseData) => {
              const response = JSON.parse(HttpService.decrypt(responseData.response))
              if (response.Status === SUCCESS){
                setCurrState(1);
              } else {
                showAlertDialog(response.Message)
              }
            })
            break;
          case 1:
            // verify otp
            if (otp.length !== 6){
                return
            }
            const postPayload1 = {'email':email, 'user_type':userType, 'otp':otp}
            HttpService.postFetch(USER_CONFIRM_IDENTITY_OTP, postPayload1)
            .then((responseData) => {
              const response = JSON.parse(HttpService.decrypt(responseData.response))
              if (response.Status === SUCCESS){
                setCurrState(2);
              } else {
                showAlertDialog(response.Message)
              }
            })
            break;
          case 2:
            // setnewpassword
            if (password === '' || password !== verifyPassword){
                return
            }
            const postPayload2 = {'email':email, 'user_type':userType, 'password':password}
            HttpService.postFetch(USER_FORGOT_PASSWORD, postPayload2)
            .then((responseData) => {
              const response = JSON.parse(HttpService.decrypt(responseData.response))
              if (response.Status === SUCCESS){
                setCurrState(2);
                showAlertDialog(response.Message)
                setTimeout(()=>navigate('/patient/userprofile'), 3000);
              } else {
                showAlertDialog(response.Message)
              }
            })
      }
    }
    
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

    return (
      <div>
        <div className="d-flex align-items-center auth px-0">
          <div className="row w-100 h-100 mx-0 my-5">
            <div className="col-lg-6 mx-auto">
              <div className="auth-form-light text-left py-5 px-4 px-sm-5">
                <div className="brand-logo" >
                  <img src={icon} alt="logo" />
                </div>
                <h6 className="font-weight-light">Reset Password</h6>
                <Form className="pt-3" onSubmit={handleSubmit}>
                  <Form.Group className="d-flex search-field" >
                    <Form.Control type="email" placeholder="Email" size="lg" className="h-auto" onChange={(event)=>setEmail(event.target.value)} disabled={currState !== 0}/>
                  </Form.Group>
                  <Form.Group className="d-flex mt-1">
                    <Form.Select id="userSelect" onChange={(e)=>setUserType(e.target.value)} required disabled={currState !== 0}>
                        <option defaultValue={0}>Select user type</option>
                        <option value={1}>Patient</option>
                        <option value={2}>Hospital Staff</option>
                        <option value={3}>Doctor</option>
                        <option value={4}>Lab Staff</option>
                        <option value={5}>Insurance Staff</option>
                        <option value={6}>Admin</option>
                    </Form.Select>
                  </Form.Group>
                  <div style={{display:(currState >= 1 ? 'block' : 'none')}}>
                    <Form.Group className="search-field mt-1"> 
                        <Form.Control type="numeric" placeholder="OTP (use virtual keyboard)" size="lg" className="h-auto mb-1" maxLength={6} value={otp} disabled={currState !== 1}/>
                        <div style={{display: (currState === 1 ? 'block': 'none')}}>
                            <Keyboard
                            layoutName={layoutName}
                            maxLength={6}
                            onChange={(val) => setOtp(val)}
                            onKeyPress={onKeyPress}
                            />
                        </div>
                    </Form.Group>
                  </div>
                  <div style={{display:(currState === 2 ? 'block' : 'none')}}>
                    <Form.Group className="d-flex search-field mt-1">
                        <Form.Control type="password" placeholder="new password" size="lg" className="h-auto" maxLength={12} onChange={(event)=>setPassword(event.target.value)} isInvalid={password === ''}/>
                    </Form.Group>
                    <Form.Group className="search-field mt-1">
                        <Form.Control type="password" placeholder="re-enter password" size="lg" className="h-auto" maxLength={12} onChange={(event)=>setVerifyPassword(event.target.value)} isInvalid={password !== verifyPassword}/>
                    </Form.Group>
                  </div>
                  <div className="mt-3 w-100 mx-auto d-flex flex-column">
                    <Button className="btn btn-block btn-primary btn-lg font-weight-medium auth-form-btn" variant="primary" type="submit">
                        {
                            currState === 0? "SEND OTP" : 
                            currState === 1? "VERIFY OTP":
                            "RESET PASSWORD"
                        }
                    </Button>
                  </div>
                </Form>
              </div>
            </div>
          </div>
        </div>  
        <Alert show={showAlert} variant='danger' style={{"position":"sticky", "bottom":"1rem", "width":"100%"}}>
            <span style={{color:"red", fontWeight:"bolder"}}>{alertMsg}</span>
        </Alert>
      </div>
    )
  }

