import React, {useState}  from 'react';
import { Form, Button } from 'react-bootstrap';
import { CREATE_UPDATE_LAB_REPORT } from '../../Constants/PathConstants';
import { SUCCESS } from '../../Constants/StringConstant';
import HttpService from '../../Services/HttpService';

export default function LabTestReports(props) {

  const [ID, setID] = useState("")
  const [textarea1, setTextarea1] = useState("");
  
  const handleSubmit = (event) => {
    const payloadJson = {
      "appointment_id": ID,
      "lab_report": textarea1
    }
    HttpService.postFetch(CREATE_UPDATE_LAB_REPORT, payloadJson)
    .then((responseData) => 
    {
        const response = JSON.parse(HttpService.decrypt(responseData.response))
        if (response.Status === SUCCESS){
            props.showAlertDialog(response.Message)
          } else {
            props.showAlertDialog(response.Message)
          }
    })
  }

return (
  <div>
  <div className="row">
    <div className="col-12 grid-margin">
      <div className="card">
        <div className="card-body">
          <form className="form-sample">
          
            <div className="row">
              <div className="col-md-12">
                <Form.Group className="row" style={{alignItems:'center'}}>
                  <label className="col-sm-2 col-form-label">Appointment ID</label>
                  <div className="col-sm-3" style={{height:'min-content'}}>
                  <Form.Control type="numeric" value={ID} className="h-auto" maxLength={8} onChange={(event)=>setID(event.target.value)}/>
                  </div>
                </Form.Group>
              </div>
            </div>

            <div className="row mt-4">
              <div className="col-md-12">
                <Form.Group className="row form-horizontal" style={{alignItems:'center'}}>
                  <label className="col-sm-2 col-form-label">Lab report</label>
                  <div className="col-sm-6" style={{height:'min-content'}}>
                  <Form.Control as="textarea" value={textarea1} rows={10}  className="h-auto" onChange={(event)=>setTextarea1(event.target.value)}/>
                  </div>
                </Form.Group>
              </div>
            </div>
          
            <div>
              <div className="row mt-5 col-sm-2 d-flex flex-column">
              <Button className="btn btn-block btn-primary btn-lg font-weight-medium auth-form-btn" variant="primary" onClick={handleSubmit}>{"SUBMIT"}</Button>
              </div>
            </div>

          </form>
        </div>
      </div>
    </div>
  </div>
  </div>

  )
}