import React, { useState, useEffect } from 'react';
import { Form, Button, input, table } from 'react-bootstrap';
import { UserContext } from "../ContextProvider";
import Button1 from '@mui/material/Button';
import { DropdownButton } from 'react-bootstrap';
import { Dropdown } from 'react-bootstrap';
import DeleteIcon from '@mui/icons-material/Delete';
import EditIcon from '@mui/icons-material/Delete';
import Keyboard from "react-simple-keyboard";
import "../../../node_modules/react-simple-keyboard/build/css/index.css";
import HttpService from '../../Services/HttpService';
import {INITIATE_TRANSACTION, GET_TRANSACTIONS_TO_INITIATE, REJECT_APPOINTMENTS} from "../../Constants/PathConstants";
import {SUCCESS} from "../../Constants/StringConstant"

export default function Transactions(props){
    const [transactionList, setTransactionList] = useState([])
    const [amount, setAmount] = useState({})
    const [reason, setReason] = useState({})
    const [insurance, setInsurance] = useState({})

    useEffect(()=> {
        setTransactionLists()
    }, [])

    const setTransactionLists = () => {
        HttpService.postFetch(GET_TRANSACTIONS_TO_INITIATE, {})
        .then((responseData) => 
        {
            const response = JSON.parse(HttpService.decrypt(responseData.response))
            if (response.Status === SUCCESS){
                setTransactionList(response.Data)
                setAmount({})
                setReason({})
                setInsurance({})
              } else {
                props.showAlertDialog(response.Message)
              }
        })
    }
    const onSubmit = (value) => {
        if (!(!!amount[value.transaction_id] && !!reason[value.transaction_id] && !!insurance[value.transaction_id])){
            props.showAlertDialog("Please fill/select all the fields")
            return
        }
        if(insurance[value.transaction_id] !== "1" && insurance[value.transaction_id] !== "2"){
            props.showAlertDialog("Please select paid by option")
            return
        }
        const postJson = {
            "transaction_id": value.transaction_id,
            "transaction_amount": amount[value.transaction_id],
            "reason": reason[value.transaction_id],
            "appointment_id": value.appointment_id,
            "transaction_type": insurance[value.transaction_id] == "1"? "Self" : "Insurance"
        }
        HttpService.postFetch(INITIATE_TRANSACTION, postJson)
        .then((responseData) => 
        {
            const response = JSON.parse(HttpService.decrypt(responseData.response))
            if (response.Status === SUCCESS){
                props.showAlertDialog(response.Message)
                setTransactionLists()
              } else {
                props.showAlertDialog(response.Message)
              }
        })
    }

    const setAmountArr = (value, id) => {
        setAmount({...amount, [id]:value})
    }
    const setReasonArr = (value, id) => {
        setReason({...reason, [id]:value})
    }
    const setInsuranceArr = (value, id) => {
        setInsurance({...insurance, [id]:value})
    }

    return(

        <div className="row">

            <div className="col-lg-12 grid-margin mt-4 stretch-card" >
                <div className="card">
                    <div className="card-body">
                    <h4 className="card-title">Transactions to initiate</h4>
                    {
                        transactionList.length === 0  ?
                        <p className="card-description"> No transactions to initiate </p> :
                            (
                                <div>  
                                    {
                                        transactionList.length !== 0 && (
                                            <div style={{marginTop:"3rem"}}>
                                              
                                                <div className='table-responsive'>
                                                    <table className='table'>
                                                        <thead>
                                                            <tr>
                                                                <th>Transaction #</th>
                                                                <th>Patient email</th>
                                                                <th>Amount</th>
                                                                <th>Reason</th>
                                                                <th>Paid by</th>
                                                                <th></th>
                                                            </tr>
                                                        </thead>
                                                        <tbody>
                                                            {
                                                                Object.entries(transactionList).map(([key,value]) => {
                                                                    return (
                                                                        <tr>
                                                                            <td className="col-md-1">{value.transaction_id}</td>
                                                                            <td className="col-md-1">{value.email}</td>
                                                                            <td className="col-md-2">
                                                                                <Form.Control type="number" rows={1}  className="h-auto" value={!!amount[value.transaction_id]?amount[value.transaction_id]:""} onChange={(event)=>setAmountArr(event.target.value, value.transaction_id)}/>
                                                                            </td>
                                                                            <td className="col-md-5">
                                                                                <Form.Control as="textarea" rows={4}  className="h-auto" value={!!reason[value.transaction_id]?reason[value.transaction_id]:""}  onChange={(event)=>setReasonArr(event.target.value, value.transaction_id)}/>
                                                                            </td>
                                                                            <td className='col-md-2'>
                                                                                <Form.Group className="d-flex mt-1">
                                                                                    <Form.Select id="userSelect" style={{fontSize:"80%"}} value={!!insurance[value.transaction_id]?insurance[value.transaction_id]:""}  onChange={(event)=>setInsuranceArr(event.target.value, value.transaction_id)} required>
                                                                                        <option defaultValue={0}>Paid By</option>
                                                                                        <option value={1}>Self</option>
                                                                                        <option value={2}>Insurance</option>
                                                                                    </Form.Select>
                                                                                </Form.Group>
                                                                            </td>

                                                                            <td className="col-md-1">
                                                                                <Button className="btn btn-block btn-primary col-md-12 font-weight-medium"
                                                                                    variant="primary"
                                                                                    type="button"
                                                                                    disabled={!amount[value.transaction_id] && !reason[value.transaction_id]}
                                                                                    onClick={(e)=>onSubmit(value)}>Submit</Button>
                                                                            </td>
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