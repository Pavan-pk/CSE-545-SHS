import React, { useState, useEffect } from 'react';
import { Form, Button, input } from 'react-bootstrap';
import { UserContext } from "../ContextProvider";
import HttpService from "../../Services/HttpService";
import { GET_INSURANCE_DATA, UPDATE_INSURANCE_DATA } from '../../Constants/PathConstants';
import { SUCCESS } from '../../Constants/StringConstant';

export default function Dashboard(props) {
  const {username, userEmail, userDob, userid, usertype} = React.useContext(UserContext);
  const [editing, toggleEdit] = useState(false)
  const [dob, setDob] = useState("")
  const [email, setEmail] = useState(userEmail)
  const [userName, setUserName] = useState(username)
  const [insuranceId, setInsuranceId] = useState("")
  const [validity, setValidity] = useState("")
  const [renew, setRenew] = useState("")

  useEffect(()=> {
    setInsuranceDetails({})
  }, [])

  const setInsuranceDetails = () => {
      const payloadJson = {
          "user_id":userid,
      }
      HttpService.postFetch(GET_INSURANCE_DATA, payloadJson)
      .then((responseData) => {
        const response = JSON.parse(HttpService.decrypt(responseData.response))
        if (response.Status === SUCCESS){
            setValidity(response.Data.validity_date)
            setRenew(response.Data.renew_date)
            setInsuranceId(response.Data.insurance_id)
        } else {
          props.showAlertDialog(response.Message)
        }
      })
  }

  const onSubmit = () => {
    const payloadJson = {
        "user_id": userid,
        "user_type": usertype,
        "insurance_id": insuranceId,
        "validity_date": validity,
        "renew_date": renew
    }
    HttpService.postFetch(UPDATE_INSURANCE_DATA, payloadJson)
    .then((responseData) => {
        const response = JSON.parse(HttpService.decrypt(responseData.response))
        if (response.Status === SUCCESS){
          props.showAlertDialog(response.Message)
          toggleEdit(false)
        } else {
          props.showAlertDialog(response.Message)
        }
      })
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
                    <Form.Group className="row" style={{alignItems:'center', justifyContent:'space-between', paddingRight:'5rem'}}>
                    <p className="col-sm-3 card-description"> Insurance Info </p>
                    <Button className="btn col-sm-2 btn-block btn-primary font-weight-medium"
                            variant="primary"
                            type="button"
                            disabled={editing}
                            onClick={(e)=>toggleEdit(!editing)}>EDIT</Button>
                    </Form.Group>
                  
                  </div>
                </div>
                <div className="row">
                  <div className="col-md-12">
                    <Form.Group className="row" style={{alignItems:'center'}}>
                      <label className="col-sm-3 col-form-label">User ID</label>
                      <div className="col-sm-3" style={{height:'min-content'}}>
                        <span style={{fontSize:"80%"}}>{userid}</span>
                      </div>
                    </Form.Group>
                  </div>
                </div>
                <div className="row">
                  <div className="col-md-12">
                    <Form.Group className="row form-horizontal" style={{alignItems:'center'}}>
                      <label className="col-sm-3 col-form-label">Email</label>
                      <div className="col-sm-4" style={{height:'min-content'}}>
                        <Form.Control type="email" value={email} onChange={(e) => setEmail(e.target.value)} disabled/>
                      </div>
                    </Form.Group>
                  </div>
                </div>
                <div className="row">
                  <div className="col-md-12">
                    <Form.Group className="row form-horizontal" style={{alignItems:'center'}}>
                      <label className="col-sm-3 col-form-label">Full Name</label>
                      <div className="col-sm-4" style={{height:'min-content'}}>
                        <Form.Control type="text" value={userName} onChange={(e) => setUserName(e.target.value)} disabled/>
                      </div>
                    </Form.Group>
                  </div>
                </div>
                <div className="row">
                  <div className="col-md-12">
                    <Form.Group className="row form-horizontal" style={{alignItems:'center'}}>
                      <label className="col-sm-3 col-form-label">Insurance id</label>
                      <div className="col-sm-4" style={{height:'min-content'}}>
                        <Form.Control type="text" value={insuranceId} onChange={(e) => setInsuranceId(e.target.value)} disabled={!editing}/>
                      </div>
                    </Form.Group>
                  </div>
                </div>
                <div className="row">
                  <div className="col-md-12">
                    <Form.Group className="row form-horizontal" style={{alignItems:'center'}}>
                      <label className="col-sm-3 col-form-label">Validity </label>
                      <div className="col-sm-4" style={{height:'min-content'}}>
                        <Form.Control type="date" value={renew} onChange={(e) => setRenew(e.target.value)} disabled={!editing}/>
                      </div>
                    </Form.Group>
                  </div>
                </div>
                <div className="row">
                  <div className="col-md-12">
                    <Form.Group className="row form-horizontal" style={{alignItems:'center'}}>
                      <label className="col-sm-3 col-form-label">Renew Date </label>
                      <div className="col-sm-4" style={{height:'min-content'}}>
                        <Form.Control type="date" value={validity} onChange={(e) => setValidity(e.target.value)} disabled={!editing}/>
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
                <div className="row">
                  <div className="col-md-12">
                    <Form.Group className="row form-horizontal" style={{alignItems:'center'}}>
                      <label className="col-sm-3 col-form-label">User Type</label>
                      <div className="col-sm-4" style={{height:'min-content'}}>
                        <span style={{fontSize:"80%"}}>Patient</span>
                      </div>
                    </Form.Group>
                  </div>
                </div>
                {/* <div className="row">
                  <div className="col-md-12">
                    <Form.Group className="row form-horizontal" style={{alignItems:'center'}}>
                      <label className="col-sm-3 col-form-label">Insurance ID</label>
                      <div className="col-sm-4" style={{height:'min-content'}}>
                        <Form.Control type="number" value={insuranceId} disabled={!editing} onChange={(e)=>setInsuranceId(e.target.value)}/>
                      </div>
                    </Form.Group>
                  </div>
                </div> */}
                <div style={{display:(editing ? 'block' : 'none')}}>
                  <div className="row mt-5 col-sm-2 d-flex flex-column">
                    <Button className="btn btn-block btn-primary btn-lg font-weight-medium auth-form-btn"
                            variant="primary" onClick={onSubmit}>SUBMIT</Button>
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
