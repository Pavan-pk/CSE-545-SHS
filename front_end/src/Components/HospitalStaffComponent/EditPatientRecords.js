import React, { useState } from 'react';
import { Form, Button, input } from 'react-bootstrap';
import { UserContext } from "../ContextProvider";
import HttpService from '../../Services/HttpService';
import { GET_PATIENT_FROM_EMAIL, UPDATE_PATIENT_INFO } from '../../Constants/PathConstants';
import { SUCCESS } from '../../Constants/StringConstant';
import { propTypes } from 'react-bootstrap/esm/Image';

export default function EditPatientRecords(props) {
  const {username, userContact, userEmail, userDob, userGender} = React.useContext(UserContext);
  const [editing, toggleEdit] = useState(false)
  const [speciality, setUserSpeciality] = useState('')
  const [dob, setDob] = useState('')
  const [email, setEmail] = useState('')
  const [userName, setUserName] = useState('')
  const [display, toggleDisplay] = useState(false)
  const [usertype, setUserType] = useState("0")
  const [ID, setID] = useState("")
  const [insuranceId, setInsuranceId] = useState("")

  const onSubmit = (event) => {
    event.preventDefault();
    updateUserDetails();
    toggleEdit(false)
  }

  const setUserDetails = (userDetails) => {
    setEmail(userDetails.email)
    setUserName(userDetails.full_name)
    setDob(userDetails.birth_date)
    setUserSpeciality(userDetails.user_speciality)
    setUserType(userDetails.user_type)
    toggleDisplay(true)
  }
  const getUserDetails = () => {
    const postJson = {"email" : ID}
    HttpService.postFetch(GET_PATIENT_FROM_EMAIL, postJson)
    .then((responseData) => {
      const response = JSON.parse(HttpService.decrypt(responseData.response))
      if(response.Status === SUCCESS){
        setUserDetails(response.Data.Data)
      } else {
        props.showAlertDialog(response.Message)
      }
    })
  }

  const updateUserDetails = () => {
    var payloadJson = {
      'email': email,
      'birth_date': dob,
      'full_name': userName,
      'user_type': usertype,
      'user_speciality': "",
    }
    HttpService.postFetch(UPDATE_PATIENT_INFO, payloadJson)
    .then((responseData) => {
      const response = JSON.parse(HttpService.decrypt(responseData.response))
      if (response.Status === SUCCESS){
        props.showAlertDialog(response.Message)
        toggleDisplay(false)
      } else {
        props.showAlertDialog(response.Message)
      }
    })
  }


  return(
    <div>
        <div className="row">

        <div className="col-md-12">
        <Form.Group className="row" style={{alignItems:'center'}}>

            <label className="col-sm-2 col-form-label">Patient Email</label>

            <div className="col-sm-3" style={{height:'min-content'}}>
              <Form.Control type="email"  className="h-auto" onChange={(event)=>setID(event.target.value)}/>
            </div>

            <div className="col-sm-3" style={{height:'min-content'}}>
            <Form.Group className="row" style={{alignItems:'center', justifyContent:'space-between', paddingRight:'5rem'}}>
            <Button className="btn col-sm-5 btn-block btn-primary font-weight-medium"
                        variant="primary"
                        type="button"
                        onClick={(e)=>getUserDetails()}>SUBMIT</Button>
            </Form.Group>
            </div>

        </Form.Group>
        </div>

        </div>

      <div className="row" style={{display:(display ? 'block' : 'none')}}>
        <div className="col-12 grid-margin">
          <div className="card">
            <div className="card-body">
              <form className="form-sample">
              <div className="row">
                  <div className="col-md-12">
                    <Form.Group className="row" style={{alignItems:'center', justifyContent:'space-between', paddingRight:'5rem'}}>
                    <p className="col-sm-3 card-description"> Patient info </p>
                    <Button className="btn col-sm-2 btn-block btn-primary font-weight-medium"
                            variant="primary"
                            type="button"
                            onClick={(e)=>toggleEdit(!editing)}>EDIT</Button>
                    </Form.Group>
                  </div>
                </div>
                <div className="row">
                  <div className="col-md-12">
                    <Form.Group className="row form-horizontal" style={{alignItems:'center'}}>
                      <label className="col-sm-3 col-form-label">Email</label>
                      <div className="col-sm-4" style={{height:'min-content'}}>
                        <Form.Control type="email" value={email} onChange={(e) => setEmail(e.target.value)} disabled={!editing}/>
                      </div>
                    </Form.Group>
                  </div>
                </div>
                <div className="row">
                  <div className="col-md-12">
                    <Form.Group className="row form-horizontal" style={{alignItems:'center'}}>
                      <label className="col-sm-3 col-form-label">Full Name</label>
                      <div className="col-sm-4" style={{height:'min-content'}}>
                        <Form.Control type="text" value={userName} onChange={(e) => setUserName(e.target.value)} disabled={!editing}/>
                      </div>
                    </Form.Group>
                  </div>
                </div>
                <div className="row">
                  <div className="col-md-12">
                    <Form.Group className="row form-horizontal" style={{alignItems:'center'}}>
                      <label className="col-sm-3 col-form-label">Date of Birth</label>
                      <div className="col-sm-4" style={{height:'min-content'}}>
                        <Form.Control type="date" value={dob} onChange={(e) => setDob(e.target.value)} disabled={!editing}/>
                      </div>
                    </Form.Group>
                  </div>
                </div>
                {/* <div className="row" >
                  <div className="col-md-12">
                    <Form.Group className="row" style={{alignItems:'center'}}>
                      <label className="col-sm-3 col-form-label"> User speciality</label>
                      <div className="col-sm-3" style={{height:'min-content'}}>
                        <Form.Control type="text" value={speciality} onChange={(e) => setEmail(e.target.value)} disabled={!editing}/>
                      </div>
                    </Form.Group>
                  </div>
                </div> */}
                {/* <div className="row">
                  <div className="row col-md-12 btn-group-toggle" >
                      <label className="col-sm-3 col-form-label">Gender</label>
                      <div className="col-sm-2 custom-control custom-radio custom-control-inline">
                        <input type="radio" id="customRadioInline1" name="customRadioInline1"
                              className="custom-control-input" checked={genderValue==='0'}
                              disabled={!editing} onChange={(e)=>setUserGender('0')}/>
                        <label className="custom-control-label" for="customRadioInline1" style={{marginLeft:'.5rem'}}>Male</label>
                      </div>
                      <div className="col-sm-2 custom-control custom-radio custom-control-inline">
                        <input type="radio" id="customRadioInline2" name="customRadioInline1"
                              className="custom-control-input" checked={genderValue==='1'}
                              disabled={!editing} onChange={(e)=>setUserGender('1')}/>
                        <label className="custom-control-label" for="customRadioInline2" style={{marginLeft:'.5rem'}}>Female</label>
                      </div>
                      <div className="col-sm-2 custom-control custom-radio custom-control-inline">
                        <input type="radio" id="customRadioInline3" name="customRadioInline1"
                              className="custom-control-input" checked={genderValue==='2'}
                              disabled={!editing} onChange={(e)=>setUserGender('2')}/>
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
{/*                 
          <div className="row">
            <div className="col-md-12">
              <Form.Group className="row form-horizontal" style={{alignItems:'center'}}>
                <label className="col-sm-3 col-form-label">Address</label>
                <div className="col-sm-4" style={{height:'min-content'}}>
                <Form.Control as="textarea" value={textarea} rows={5} disabled={!editing}  className="h-auto" onChange={(event)=>setTextarea(event.target.value)}/>
                </div>
              </Form.Group>
            </div>
          </div> */}
          <div style={{display:(editing ? 'block' : 'none')}}>
            <div className="row mt-5 col-sm-2 d-flex flex-column">
              <Button className="btn btn-block btn-primary btn-lg font-weight-medium auth-form-btn"
                      variant="primary" type="submit" onClick={onSubmit}>SUBMIT</Button>
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
