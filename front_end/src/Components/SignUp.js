import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import icon from '../assets/images/icon.png'
import { Form, Button, Alert } from 'react-bootstrap';
import { UserContext } from "./ContextProvider";
import { USER_REGESTRATION } from "../Constants/PathConstants";
import { SUCCESS, FAILURE, SOMETHING_WRONG } from "../Constants/StringConstant"
import HttpService from '../Services/HttpService';

export default function SignUp() {
    const [email, setEmail] = useState("")
    const [password, setPassword] = useState("")
    const [userType, setUserType] = useState(0)
    const [name, setName] = useState("")
    const [dob, setDob] = useState("")
    const [showAlert, setShowAlert] = useState(false)
    const [alertMsg, setAlertMsg] = useState('')
    const [specialist, setSpecialist] = useState('')
    const showAlertDialog = (msg) => {
      setAlertMsg(msg)
      setShowAlert(true)
      setTimeout(()=>setShowAlert(false), 3000)
    }

    const {login} = React.useContext(UserContext);
    const navigate = useNavigate();

    const validateForm = () => {
        if(email.length > 0 && password.length > 0 && name.length > 0 && dob !== ""){
          return true
        } else{
          return false
        }
    }  

    const handleSubmit = (event) => {
        event.preventDefault();
        if (validateForm()){
          const postPayload = {
            "full_name": name,
            "birth_date": dob,
            "email": email,
            "password": password,
            "user_type": userType,
            "user_speciality": userType === "3"?specialist:""
          }
          HttpService.postFetch(USER_REGESTRATION, postPayload)
          .then((responseData) => {
            const response = JSON.parse(HttpService.decrypt(responseData.response))
            if (response.Status === SUCCESS){
              navigate("/")
            } else {
              showAlertDialog(response.Message)
            }
          })
        }
    }


    return (
        <div>
          <div className="d-flex align-items-center auth px-0">
            <div className="row w-100 mx-0">
              <div className="col-lg-6 mx-auto my-5">
                <div className="auth-form-light text-left py-5 px-4 px-sm-5">
                  <div className="brand-logo">
                    <img src={icon} alt="logo" />
                  </div>
                  <h4>New here?</h4>
                  <h6 className="font-weight-light">Signing up is easy. It only takes a few steps</h6>
                  <Form className="pt-3" onSubmit={handleSubmit}>
                    <Form.Group className="d-flex search-field">
                        <Form.Control type="email" placeholder="Email"  size="lg" pattern="[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,4}$" title="Must contain @ in the email address" className="h-auto" onChange={(event)=>setEmail(event.target.value)} />
                    </Form.Group>
                    <Form.Group className="d-flex search-field mt-1">
                        <Form.Control type="password" placeholder="Password" size="lg" pattern="(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}" title="Must contain at least 1 number, 1 uppercase, 1 lowercase letter, and at least 8 or more characters" className="h-auto" maxLength={12} onChange={(event)=>setPassword(event.target.value)}/>
                    </Form.Group>
                    <Form.Group className="d-flex flex-row search-field mt-1">
                        <Form.Control type="text" placeholder="Name" size="lg" className="h-auto mx-1" onChange={(event)=>setName(event.target.value)}/>
                        <Form.Control type="date" placeholder="Date of Birth" size="lg" className="h-auto mx-1" onChange={(event)=>setDob(event.target.value)}/>
                    </Form.Group>
                    <Form.Group className="d-flex mt-1">
                        <Form.Select id="userSelect" onChange={(e)=>setUserType(e.target.value)} required>
                            <option defaultValue={0}>Select user type</option>
                            <option value={1}>Patient</option>
                            <option value={2}>Hospital Staff</option>
                            <option value={3}>Doctor</option>
                            <option value={4}>Lab Staff</option>
                            <option value={5}>Insurance Staff</option>
                            <option value={6}>Admin</option>
                        </Form.Select>
                    </Form.Group>
                    <div style={{display:userType==="3"?"block":"none"}}>
                      <Form.Group className="d-flex search-field mt-1">
                          <Form.Control type="text" placeholder="Specialist in"  size="lg" className="h-auto" onChange={(event)=>setSpecialist(event.target.value)} />
                      </Form.Group>
                    </div>
                    <div className="mt-3 w-100 mx-auto d-flex flex-column">
                        <Button className="btn btn-block btn-primary btn-lg font-weight-medium auth-form-btn" variant="primary" type="submit">{"SIGN UP"}</Button>
                    </div>
                    <div className="text-center mt-4 font-weight-light">
                      Already have an account? <Link to="/" className="text-primary">Login</Link>
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
