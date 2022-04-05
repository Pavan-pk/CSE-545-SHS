import React, { useState } from 'react';
import { Form, Button, input } from 'react-bootstrap';
import { UserContext } from "../ContextProvider";

export default function HospitalStaffProfile() {
  const {username, userEmail, userDob, userid} = React.useContext(UserContext);

  return(
    <div>
      <div className="row">
        <div className="col-12 grid-margin">
          <div className="card">
            <div className="card-body">
              <form className="form-sample">
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
                      <label className="col-sm-3 col-form-label">Full Name</label>
                      <div className="col-sm-3" style={{height:'min-content'}}>
                      <span style={{fontSize:"80%"}}>{username}</span>
                      </div>
                    </Form.Group>
                  </div>
                </div>

                {/* <div className="row">
                  <div className="col-md-12">
                    <Form.Group className="row form-horizontal" style={{alignItems:'center'}}>
                      <label className="col-sm-3 col-form-label">Designation</label>
                      <div className="col-sm-3" style={{height:'min-content'}}>
                        <span>Desk Assistant</span>
                      </div>
                    </Form.Group>
                  </div>
                </div> */}
                <div className="row">
                  <div className="col-md-12">
                    <Form.Group className="row form-horizontal" style={{alignItems:'center'}}>
                      <label className="col-sm-3 col-form-label">Email</label>
                      <div className="col-sm-3" style={{height:'min-content'}}>
                      <span style={{fontSize:"80%"}}>{userEmail}</span>
                      </div>
                    </Form.Group>
                  </div>
                </div>

                <div className="row">
                  <div className="col-md-12">
                    <Form.Group className="row form-horizontal" style={{alignItems:'center'}}>
                      <label className="col-sm-3 col-form-label">Date of Birth</label>
                      <div className="col-sm-3" style={{height:'min-content'}}>
                      <span style={{fontSize:"80%"}}>{userDob}</span>
                      </div>
                    </Form.Group>
                  </div>
                </div>
                {/* <div className="row">
                  <div className="col-md-12">
                    <Form.Group className="row form-horizontal" style={{alignItems:'center'}}>
                      <label className="col-sm-3 col-form-label">Gender</label>
                      <div className="col-sm-3" style={{height:'min-content'}}>
                        <span>{genderValue==='0'?"Male":genderValue==='1'?"Female":"Others"}</span>
                      </div>
                    </Form.Group>
                  </div>
                </div> */}
                {/* <div className="row">
                  <div className="col-md-12">
                    <Form.Group className="row form-horizontal" style={{alignItems:'center'}}>
                      <label className="col-sm-3 col-form-label">Contact</label>
                      <div className="col-sm-3" style={{height:'min-content'}}>
                        <span>{contactValue}</span>
                      </div>
                    </Form.Group>
                  </div>
                </div> */}
              </form>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
