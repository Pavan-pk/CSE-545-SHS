import React, { useState } from 'react';
import { Form, Button } from 'react-bootstrap';
import HttpService from '../../Services/HttpService';
import "../../../node_modules/react-simple-keyboard/build/css/index.css";
import { CREATE_UPDATE_LAB_REPORT, GET_LAB_RECORD_BY_APPOINTMENT_ID } from '../../Constants/PathConstants';
import { SUCCESS } from '../../Constants/StringConstant';

export default function EditLabRecords(props){
    const [ID, setID] = useState("")
    const [textarea, setTextarea] = useState("");
    const [gotRecord, setGotRecord] = useState(false)
    const [display, setDisplay] = useState(false)
    const [submitted, setSubmitted] = useState(false)
    const getRecord = () => {
        const postJson = {
            "appointment_id": ID
        }
        HttpService.postFetch(GET_LAB_RECORD_BY_APPOINTMENT_ID, postJson)
        .then((responseData) => {
          const response = JSON.parse(HttpService.decrypt(responseData.response))
          if (response.Status === SUCCESS){
              setTextarea(response.Data.lab_report)
              setGotRecord(true)
              setDisplay(true)
          } else {
            props.showAlertDialog(response.Message)
          }
        })
    }

    const handleSubmit = () => {
        const payloadJson = {
          "appointment_id": ID,
          "lab_report": textarea
        }
        HttpService.postFetch(CREATE_UPDATE_LAB_REPORT, payloadJson)
        .then((responseData) => 
        {
            const response = JSON.parse(HttpService.decrypt(responseData.response))
            if (response.Status === SUCCESS){
                props.showAlertDialog(response.Message)
                setSubmitted(true)
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

                    <label className="col-sm-2 col-form-label">Lab record ID</label>

                    <div className="col-sm-3" style={{height:'min-content'}}>
                    <Form.Control type="numeric"  className="h-auto" maxLength={8} onChange={(event)=>setID(event.target.value)}/>
                    </div>

                    <div className="col-sm-3" style={{height:'min-content'}}>
                    <Form.Group className="row" style={{alignItems:'center', justifyContent:'space-between', paddingRight:'5rem'}}>
                    <Button className="btn col-sm-5 btn-block btn-primary font-weight-medium"
                                variant="primary"
                                type="button"
                                onClick={(e)=>getRecord()}>SEARCH</Button>
                    </Form.Group>
                    </div>

                </Form.Group>

                </div>

            </div>

            <div className="col-lg-12 grid-margin mt-4 stretch-card" style={{display:display?"block":"none"}}>
                <div className="card">
                    <div className="card-body">
                    <h4 className="card-title">Records</h4>
                    <div className="row mt-4" style={{display:gotRecord?"block":"none"}}>
                        <div className="col-md-12">
                            <Form.Group className="row form-horizontal" style={{alignItems:'center'}}>
                                <label className="col-sm-2 col-form-label">Lab record</label>
                                <div className="col-sm-6" style={{height:'min-content'}}>
                                <Form.Control as="textarea" value={textarea} rows={15}  className="h-auto" disabled={submitted} onChange={(event)=>setTextarea(event.target.value)}/>
                                </div>
                            </Form.Group>
                            </div>
                        </div>
                        <div className="row mt-4" >
                            <Button className="btn btn-block btn-primary col-md-2 font-weight-medium mt-1"
                                                variant="primary"
                                                type="button"
                                                disabled={submitted}
                                                onClick={(e) => handleSubmit()}>
                                                    Submit
                            </Button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    )}