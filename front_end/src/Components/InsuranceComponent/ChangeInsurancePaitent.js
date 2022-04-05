import React, { useState } from 'react';
import { Form, Button, input } from 'react-bootstrap';
import { UserContext } from "../ContextProvider";
import HttpService from '../../Services/HttpService';
import { GET_INSURANCE_RECORD_INSURANCE_ID, UPDATE_INSURANCE_DATA } from '../../Constants/PathConstants';
import { SUCCESS } from '../../Constants/StringConstant';
import { propTypes } from 'react-bootstrap/esm/Image';

export default function ChangeInsurancePatient(props) {
  const [editing, toggleEdit] = useState(false)
  const [ID, setID] = useState("")
  const [insuranceId, setInsuranceId] = useState("")
  const [userID, setUserId] = useState("")
  const [renewDate, setRenewDate] = useState("")
  const [validityDate, setValidityDate] = useState("")
  const [display, setDisplay] = useState(false)

  const onSubmit = (event) => {
    event.preventDefault();
    updateInsurance();
    toggleEdit(false)
  }

  const get_insurance_details = () => {
    HttpService.postFetch(GET_INSURANCE_RECORD_INSURANCE_ID, {"insurance_id":ID})
    .then((responseData) => {
        const response = JSON.parse(HttpService.decrypt(responseData.response))
        if (response.Status === SUCCESS){
            setDisplay(true)
            setUserId(response.Data.user_id)
            setInsuranceId(response.Data.insurance_id)
            setRenewDate(response.Data.renew_date)
            setValidityDate(response.Data.validity_date)
        } else {
            props.showAlertDialog(response.Message)
    }})

  }
  const updateInsurance = () => {
    const payloadJson = {
        "user_id": userID,
        "insurance_id": insuranceId,
        "validity_date": validityDate,
        "renew_date": renewDate
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

        <div className="col-md-12">
        <Form.Group className="row" style={{alignItems:'center'}}>

            <label className="col-sm-2 col-form-label">Insurance ID</label>

            <div className="col-sm-3" style={{height:'min-content'}}>
              <Form.Control type="email"  className="h-auto" onChange={(event)=>setID(event.target.value)}/>
            </div>

            <div className="col-sm-3" style={{height:'min-content'}}>
            <Form.Group className="row" style={{alignItems:'center', justifyContent:'space-between', paddingRight:'5rem'}}>
            <Button className="btn col-sm-5 btn-block btn-primary font-weight-medium"
                        variant="primary"
                        type="button"
                        onClick={(e)=>(get_insurance_details())}>SUBMIT</Button>
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
                      <label className="col-sm-3 col-form-label">Insurance ID</label>
                      <div className="col-sm-4" style={{height:'min-content'}}>
                        <Form.Control type="email" value={insuranceId} onChange={(e) => setInsuranceId(e.target.value)} disabled/>
                      </div>
                    </Form.Group>
                  </div>
                </div>
                <div className="row">
                  <div className="col-md-12">
                    <Form.Group className="row form-horizontal" style={{alignItems:'center'}}>
                      <label className="col-sm-3 col-form-label">User ID</label>
                      <div className="col-sm-4" style={{height:'min-content'}}>
                        <Form.Control type="text" value={userID} onChange={(e) => setUserId(e.target.value)} disabled/>
                      </div>
                    </Form.Group>
                  </div>
                </div>
                <div className="row">
                  <div className="col-md-12">
                    <Form.Group className="row form-horizontal" style={{alignItems:'center'}}>
                      <label className="col-sm-3 col-form-label">Renew Date</label>
                      <div className="col-sm-4" style={{height:'min-content'}}>
                        <Form.Control type="date" value={renewDate} onChange={(e) => setRenewDate(e.target.value)} disabled={!editing}/>
                      </div>
                    </Form.Group>
                  </div>
                </div>
                <div className="row">
                  <div className="col-md-12">
                    <Form.Group className="row form-horizontal" style={{alignItems:'center'}}>
                      <label className="col-sm-3 col-form-label">Validity Date</label>
                      <div className="col-sm-4" style={{height:'min-content'}}>
                        <Form.Control type="date" value={validityDate} disabled={!editing} onChange={(e)=>setValidityDate(e.target.value)}/>
                      </div>
                    </Form.Group>
                  </div>
                </div>
                <div style={{display:(editing ? 'block' : 'none')}}>
                    <div className="row mt-5 col-sm-2 d-flex flex-column">
                    <Button className="btn btn-block btn-primary btn-lg font-weight-medium auth-form-btn" disabled={!editing}
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
