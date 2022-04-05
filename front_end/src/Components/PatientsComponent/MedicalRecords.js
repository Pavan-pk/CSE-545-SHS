import React, { useState, useEffect } from 'react';
import { Form, Button, input, table } from 'react-bootstrap';
import { GET_MEDICAL_RECORDS } from '../../Constants/PathConstants';
import { SUCCESS } from '../../Constants/StringConstant';
import HttpService from '../../Services/HttpService';
import { UserContext } from "../ContextProvider";

export default function MedicalRecords(props){
    const {userid} = React.useContext(UserContext);
    const [labRecords, setLabRecords] = useState([])
    const [diagnosisRecords, setDiagnosisRecords] = useState([])
    const [prescriptionRecords, setPrescriptionRecords] = useState([])
    // Ideally should get it when mounted in useEffect

    useEffect(() => {
        downloadRecord()
      }, []);

    const downloadRecord = () => {
        HttpService.postFetch(GET_MEDICAL_RECORDS, {"user_id": userid})
        .then((responseData) => {
            const response = JSON.parse(HttpService.decrypt(responseData.response))
            if (response.Status === SUCCESS){
              setDiagnosisRecords(response.DiagnosisData)
              setLabRecords(response.LabData)
              setPrescriptionRecords(response.PrescriptionData)
              props.showAlertDialog(response.Message)
            } else {
              props.showAlertDialog(response.Message)
            }
        })
    }

    return(
        <div className="row">
            <div className="col-lg-12 grid-margin stretch-card">
                <div className="card">
                    <div className="card-body">
                    <h4 className="card-title">Records</h4>
                    {
                        labRecords.length === 0 && diagnosisRecords.length === 0 && prescriptionRecords.length === 0  ?
                        <p className="card-description"> No records to show. </p> :
                            (
                                <div>
                                    {
                                    diagnosisRecords.length !== 0 && (
                                    <div style={{marginTop:"3rem"}}>
                                        <h4 className="card-title">Diagnosis Records</h4>
                                        <div className='table-responsive'>
                                            <table className='table'>
                                                <thead>
                                                    <tr>
                                                        <th>ID</th>
                                                        <th>Date</th>
                                                        <th>Record</th>
                                                    </tr>
                                                </thead>
                                                <tbody>
                                                    {
                                                        Object.entries(diagnosisRecords).map(([key,value]) => {
                                                            return (
                                                                <tr>
                                                                    <td className="col-md-1">{value.diagnosis_id}</td>
                                                                    <td className="col-md-1">{value.time}</td>
                                                                    <td className="col-md-6">{value.diagnosis_record}</td>
                                                                </tr>
                                                            )
                                                        })
                                                    }
                                                </tbody>
                                            </table>
                                        </div>
                                    </div>
                                    )
                                    }
                                    {
                                        prescriptionRecords.length !== 0 && (
                                            <div style={{marginTop:"3rem"}}>
                                                <h4 className="card-title">Prescription Records</h4>
                                                <div className='table-responsive'>
                                                    <table className='table'>
                                                        <thead>
                                                            <tr>
                                                                <th>ID</th>
                                                                <th>Date</th>
                                                                <th>Record</th>
                                                            </tr>
                                                        </thead>
                                                        <tbody>
                                                            {
                                                                Object.entries(prescriptionRecords).map(([key,value]) => {
                                                                    return (
                                                                        <tr>
                                                                            <td className="col-md-1">{value.prescription_id}</td>
                                                                            <td className="col-md-1">{value.time}</td>
                                                                            <td className="col-md-6">{value.prescription_record}</td>
                                                                        </tr>
                                                                    )
                                                                })
                                                            }
                                                        </tbody>
                                                    </table>
                                                </div>
                                            </div>
                                        )
                                    }
                                    {
                                        labRecords.length !== 0 && (
                                            <div style={{marginTop:"3rem"}}>
                                                <h4 className="card-title">Lab Records</h4>
                                                <div className='table-responsive'>
                                                    <table className='table'>
                                                        <thead>
                                                            <tr>
                                                                <th>ID</th>
                                                                <th>Date</th>
                                                                <th>Lab recommendation</th>
                                                                <th>Record</th>
                                                            </tr>
                                                        </thead>
                                                        <tbody>
                                                            {
                                                                Object.entries(labRecords).map(([key,value]) => {
                                                                    return (
                                                                        <tr>
                                                                            <td className="col-md-1">{value.lab_id}</td>
                                                                            <td className="col-md-1">{value.time}</td>
                                                                            <td className="col-md-2">{value.lab_recommendation}</td>
                                                                            <td className="col-md-5">{value.lab_report}</td>
                                                                        </tr>
                                                                    )
                                                                })
                                                            }
                                                        </tbody>
                                                    </table>
                                                </div>
                                            </div>
                                        )
                                    }
                                </div>  
                            )
                        }
                    </div>
                </div>
            </div>
        </div>);
};