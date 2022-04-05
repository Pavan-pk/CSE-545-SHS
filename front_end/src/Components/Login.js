import React, { Component, useEffect, useState, useRef } from 'react';
import { Form, Button, Alert } from 'react-bootstrap';
import icon from '../assets/images/icon.png'
import { useNavigate , Link} from "react-router-dom";
import { UserContext } from "./ContextProvider"
import Keyboard from "react-simple-keyboard";
import { CONFIRM_OTP, GET_USER_DATA, LOGIN, SEND_OTP } from '../Constants/PathConstants';
import "../../node_modules/react-simple-keyboard/build/css/index.css";

import HttpService from "../Services/HttpService";
import { SUCCESS } from '../Constants/StringConstant';


export default function Login() {
    const [askOtp, setAskOtp] = useState(false)
    const [email, setEmail] = useState("")
    const [password, setPassword] = useState("")
    const [userType, setUserType] = useState(0)
    const [otp, setOtp] = useState("")
    const [layoutName, setLayoutName] = useState("default")
    const [resetEnabled, setResetEnabled] = useState(false)
    const [showAlert, setShowAlert] = useState(false)
    const [alertMsg, setAlertMsg] = useState('')

    const {login, setHttpToken} = React.useContext(UserContext);
    const navigate = useNavigate();

    const validateForm = () => {
        if(email.length > 0 && password.length > 0){
          //validated user cred and send otp or error
          return true
        } else{
          return false
        }
    } 
    
    const showAlertDialog = (msg) => {
      setAlertMsg(msg)
      setShowAlert(true)
      setTimeout(()=>setShowAlert(false), 3000)
    }

    const sendOtp = () => {
      const requestPayload = {
        "email": email,
        "user_type": userType,
        "password":password
      }
      HttpService.postFetch(LOGIN, requestPayload)
      .then((responseData) => 
      {
        const response = JSON.parse(HttpService.decrypt(responseData.response))
        if(response.Status === SUCCESS){
          setAskOtp(true)
          setResetEnabled(false)
          setHttpToken(response.access_token)
          setTimeout(()=>setResetEnabled(true), 1000 * 60)
        }
        else {
          showAlertDialog(response.Message)
        }
      })
    }
    
    const handleSubmit = (event) => {
      event.preventDefault();
      if (!askOtp && validateForm()){
        sendOtp()
        return
      }
      if (askOtp){
        validateOtp()
      }
    }

    const setUserDataLogin = (navto, loginJson) => {
      HttpService.postFetch(GET_USER_DATA, loginJson)
      .then((responseLoginData) => {
        const responseLogin = JSON.parse(HttpService.decrypt(responseLoginData.response))
        if (responseLogin.Status === SUCCESS){
          loginJson.user_id = responseLogin.Data.user_id
          loginJson.full_name = responseLogin.Data.full_name
          loginJson.dob = responseLogin.Data.birth_date
          loginJson.user_speciality = responseLogin.Data.user_speciality
          loginJson.insurance_id = responseLogin.Data.insurance_id
          login(loginJson)
          navigate(navto)
        } else {
          showAlertDialog(responseLogin.Message)
        }
      })
    }

    const validateOtp = () => {
        if (otp.length !== 6){
            return
        }
        const requestPayload = {"otp": otp}
        HttpService.postFetch(CONFIRM_OTP, requestPayload)
        .then((responseData) => {
          const response = JSON.parse(HttpService.decrypt(responseData.response))
          if(response.Status === SUCCESS){
            var loginJson = {
              "email": email,
              "user_type": userType
            }
            switch(userType){
              case "1":
                setUserDataLogin('/patient/userprofile', loginJson)
                break
              case "2":
                setUserDataLogin('/hospitalstaff/HospitalStaffProfile', loginJson)
                break
              case "3":
                setUserDataLogin('/doctor/doctorprofile', loginJson)
                break
              case "4":
                setUserDataLogin('/lab/LabStaffProfile', loginJson)
                break
              case "5":
                setUserDataLogin('/insurance/InsuranceStaffProfile', loginJson)
                break
              case "6":
                setUserDataLogin('/admin/adminProfile', loginJson)
                break
              default:
                setUserDataLogin('/notimplemented', loginJson)
            }
          } else {
            showAlertDialog(response.Message)
          }
        })
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
                <h4>Welcome!</h4>
                <h6 className="font-weight-light">Sign in to continue.</h6>
                <Form className="pt-3" onSubmit={handleSubmit}>
                  <Form.Group className="d-flex search-field">
                    <Form.Control type="email" placeholder="Username" size="lg" className="h-auto" onChange={(event)=>setEmail(event.target.value)} disabled={askOtp}/>
                  </Form.Group>
                  <Form.Group className="d-flex search-field mt-1">
                    <Form.Control type="password" placeholder="Password" size="lg" className="h-auto" maxLength={12} onChange={(event)=>setPassword(event.target.value)} disabled={askOtp}/>
                  </Form.Group>
                  <div className="text-center mt-1 mb-2 font-weight-small" style={{ display:(askOtp ? 'none' : 'block'), "fontSize":"0.75rem"}}>
                    Forgot password? <Link to="/passwordreset" className="text-primary">Reset Password</Link>
                  </div>
                  <Form.Group className="d-flex mt-1">
                    <Form.Select id="userSelect" onChange={(e)=>setUserType(e.target.value)} required disabled={askOtp}>
                        <option defaultValue={0}>Select user type</option>
                        <option value={1}>Patient</option>
                        <option value={2}>Hospital Staff</option>
                        <option value={3}>Doctor</option>
                        <option value={4}>Lab Staff</option>
                        <option value={5}>Insurance Staff</option>
                        <option value={6}>Admin</option>
                    </Form.Select>
                  </Form.Group>
                  <div style={{display:(askOtp ? 'block' : 'none')}}>
                    <Form.Group className="search-field mt-1">
                        <Form.Control type="numeric" placeholder="OTP (use virtual keyboard)" size="lg" className="h-auto mb-1" maxLength={6} value={otp}/>
                        <Keyboard
                          layoutName={layoutName}
                          maxLength={6}
                          onChange={(val) => setOtp(val)}
                          onKeyPress={onKeyPress}
                        />
                        <div className="mt-3 w-100 mx-auto d-flex flex-column">
                          <Button className="btn btn-block btn-primary btn-sm col-md-4 font-weight-small auth-form-btn"
                                  variant="primary"
                                  disabled={!resetEnabled}
                                  onClick={(e)=>sendOtp()}
                                  type="button">
                                    {"Resend OTP"}
                          </Button>
                        </div>
                    </Form.Group>
                  </div>
                  <div className="mt-3 w-100 mx-auto d-flex flex-column">
                    <Button className="btn btn-block btn-primary btn-lg font-weight-medium auth-form-btn" variant="primary" type="submit">{askOtp? "SIGN IN" : "SEND OTP"}</Button>
                  </div>
                  <div className="text-center mt-2 font-weight-light">
                    Don't have an account? <Link to="/signup" className="text-primary">Create</Link>
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

