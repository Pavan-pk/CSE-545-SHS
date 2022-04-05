import React, { useState } from 'react';
import { Form, Button, input } from 'react-bootstrap';
import { UserContext } from "../ContextProvider";
import HttpService from '../../Services/HttpService';
import { USER_REGESTRATION } from '../../Constants/PathConstants';
import { SUCCESS } from '../../Constants/StringConstant';

export default function CreatePatientDiagnosis(props) {
  const [dob, setDob] = useState("")
  const [email, setEmail] = useState("")
  const [userName, setUserName] = useState("")
  const [submitted, setSubmitted] = useState(false)
  const [password, setPassword] = useState("")

  const validateForm = () => {
    if(email.length > 0 && password.length > 0 && userName.length > 0 && dob !== ""){
      return true
    } else{
      return false
    }
  } 

  const onSubmit = (event) => {
    event.preventDefault();
    if (validateForm() && !submitted){
      const postPayload = {
        "full_name": userName,
        "birth_date": dob,
        "email": email,
        "password": password,
        "user_type": "1",
        "user_speciality": ""
      }
      HttpService.postFetch(USER_REGESTRATION, postPayload)
      .then((responseData) => {
        const response = JSON.parse(HttpService.decrypt(responseData.response))
        if (response.Status === SUCCESS){
          setSubmitted(true)
          props.showAlertDialog(response.Message)
        } else {
          props.showAlertDialog(response.Message)
        }
      })
    }
    else if (submitted) {
      setDob("")
      setEmail("")
      setUserName("")
      setPassword("")
      setSubmitted(false);
    }
  }

  return(
    <div>
      <div className="row">
        <div className="col-12 grid-margin">
          <div className="card">
            <div className="card-body">
              <form className="form-sample">
              <div className="row">
                  <div className="col-md-12">
                    <Form.Group className="row" style={{alignItems:'center', justifyContent:'space-between', paddingRight:'5rem'}} disabled={submitted}>
                    <p className="col-sm-3 card-description"> Patient info </p>
                    </Form.Group>
                  </div>
                </div>
                <div className="row">
                </div>
                <div className="row">
                  <div className="col-md-12">
                    <Form.Group className="row form-horizontal" style={{alignItems:'center'}}>
                      <label className="col-sm-3 col-form-label">Email</label>
                      <div className="col-sm-4" style={{height:'min-content'}}>
                        <Form.Control type="email" value={email} onChange={(e) => setEmail(e.target.value)} disabled={submitted}/>
                      </div>
                    </Form.Group>
                  </div>
                  <div className="col-md-12">
                    <Form.Group className="row form-horizontal" style={{alignItems:'center'}}>
                      <label className="col-sm-3 col-form-label">Password</label>
                      <div className="col-sm-4" style={{height:'min-content'}}>
                        <Form.Control type="password" disabled={submitted} placeholder="Password" size="lg" pattern="(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}" title="Must contain at least 1 number, 1 uppercase, 1 lowercase letter, and at least 8 or more characters" className="h-auto" maxLength={12} onChange={(event)=>setPassword(event.target.value)}/>
                      </div>
                    </Form.Group>
                  </div>
                </div>
                <div className="row">
                  <div className="col-md-12">
                    <Form.Group className="row form-horizontal" style={{alignItems:'center'}}>
                      <label className="col-sm-3 col-form-label">Full Name</label>
                      <div className="col-sm-4" style={{height:'min-content'}}>
                        <Form.Control type="text" value={userName} onChange={(e) => setUserName(e.target.value)} disabled={submitted}/>
                      </div>
                    </Form.Group>
                  </div>
                </div>
                <div className="row">
                  <div className="col-md-12">
                    <Form.Group className="row form-horizontal" style={{alignItems:'center'}}>
                      <label className="col-sm-3 col-form-label">Date of Birth</label>
                      <div className="col-sm-4" style={{height:'min-content'}}>
                        <Form.Control type="date" value={dob} onChange={(e) => setDob(e.target.value)} disabled={submitted}/>
                      </div>
                    </Form.Group>
                  </div>
                </div>
                {/* <div className="row">
                  <div className="row col-md-12 btn-group-toggle" >
                      <label className="col-sm-3 col-form-label">Gender</label>
                      <div className="col-sm-2 custom-control custom-radio custom-control-inline">
                        <input type="radio" id="customRadioInline1" name="customRadioInline1"
                              className="custom-control-input" checked={genderValue==='0'}
                              onChange={(e)=>setUserGender('0')}/>
                        <label className="custom-control-label" for="customRadioInline1" style={{marginLeft:'.5rem'}}>Male</label>
                      </div>
                      <div className="col-sm-2 custom-control custom-radio custom-control-inline">
                        <input type="radio" id="customRadioInline2" name="customRadioInline1"
                              className="custom-control-input" checked={genderValue==='1'}
                               onChange={(e)=>setUserGender('1')}/>
                        <label className="custom-control-label" for="customRadioInline2" style={{marginLeft:'.5rem'}}>Female</label>
                      </div>
                      <div className="col-sm-2 custom-control custom-radio custom-control-inline">
                        <input type="radio" id="customRadioInline3" name="customRadioInline1"
                              className="custom-control-input" checked={genderValue==='2'}
                               onChange={(e)=>setUserGender('2')}/>
                        <label className="custom-control-label" for="customRadioInline3" style={{marginLeft:'.5rem'}}>Others</label>
                      </div>
                  </div>
                </div> */}
                {/* <div className="row">
                  <div className="col-md-12">
                    <Form.Group className="row form-horizontal" style={{alignItems:'center'}}>
                      <label className="col-sm-3 col-form-label">User Type</label>
                      <div className="col-sm-4" style={{height:'min-content'}}>
                        <span>Patient</span>
                      </div>
                    </Form.Group>
                  </div>
                </div> */}
          {/* <div className="row">
            <div className="col-md-12">
              <Form.Group className="row form-horizontal" style={{alignItems:'center'}}>
                <label className="col-sm-3 col-form-label">Address</label>
                <div className="col-sm-4" style={{height:'min-content'}}>
                <Form.Control as="textarea" value={textarea} rows={5}  className="h-auto" onChange={(event)=>setTextarea(event.target.value)}/>
                </div>
              </Form.Group>
            </div>
          </div> */}
                {/* <div className="row">
                  <div className="col-md-12">
                    <Form.Group className="row form-horizontal" style={{alignItems:'center'}}>
                      <label className="col-sm-3 col-form-label">Contact</label>
                      <div className="col-sm-4" style={{height:'min-content'}}>
                        <Form.Control type="number" value={contactValue}  onChange={(e)=>changeContact(e.target.value)}/>
                      </div>
                    </Form.Group>
                  </div>
                </div> */}
                <div>
                  <div className="row mt-5 col-sm-2 d-flex flex-column">
                    <Button className="btn btn-block btn-primary btn-lg font-weight-medium auth-form-btn"
                            variant="primary" type="submit" onClick={onSubmit}>{submitted? "Create another":"Submit"}</Button>
                  </div>
                </div>
              </form>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
