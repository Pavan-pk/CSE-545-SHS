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
import {APPROVE_REJECT_TRANSACTIONS, GET_TRANSACTIONS_TO_APPROVE} from "../../Constants/PathConstants";
import {SUCCESS} from "../../Constants/StringConstant"

export default function ApproveTransactions(props){
    const [transactionList, setTransactionList] = useState([])

    useEffect(()=> {
        setTransactions()
    }, [])

    const setTransactions = () => {
        HttpService.postFetch(GET_TRANSACTIONS_TO_APPROVE, {})
        .then((responseData) => 
        {
            const response = JSON.parse(HttpService.decrypt(responseData.response))
            if (response.Status === SUCCESS){
                if(!!response.Data){
                    setTransactionList(response.Data)
                } else {
                    setTransactionList([])
                }
              } else {
                props.showAlertDialog(response.Message)
              }
        })
    }
    const approveData = (value) => {
        const postJson = {
            "transaction_id":value.transaction_id,
            "status":"Approved"}
        HttpService.postFetch(APPROVE_REJECT_TRANSACTIONS, postJson)
        .then((responseData) => {
            const response = JSON.parse(HttpService.decrypt(responseData.response))
            if (response.Status === SUCCESS){
                setTransactions()
              } else {
                props.showAlertDialog(response.Message)
            }
        })
    }

    const rejectData = (value) => {
        const postJson = {
            "transaction_id":value.transaction_id,
            "status":"Rejected"}
        HttpService.postFetch(APPROVE_REJECT_TRANSACTIONS, postJson)
        .then((responseData) => {
            const response = JSON.parse(HttpService.decrypt(responseData.response))
            if (response.Status === SUCCESS){
                setTransactions()
                } else {
                props.showAlertDialog(response.Message)
            }
        })
    }

    return(

        <div className="row">

            <div className="col-lg-12 grid-margin mt-4 stretch-card" >
                <div className="card">
                    <div className="card-body">
                    <h4 className="card-title">Transactions</h4>
                    {
                        transactionList.length === 0  ?
                        <p className="card-description">No transactions to approve.</p> :
                            (
                                <div>  
                                    {
                                        transactionList.length !== 0 && (
                                            <div style={{marginTop:"3rem"}}>
                                              
                                                <div className='table-responsive'>
                                                    <table className='table'>
                                                        <thead>
                                                            <tr>
                                                                <th>Transaction ID</th>
                                                                <th>Email</th>
                                                                <th>Transaction Reason</th>
                                                                <th></th>
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
                                                                            <td className="col-md-5">{value.reason}</td>
                                                                            <td className="col-md-1">
                                                                                <Button className="btn btn-block btn-primary col-md-12 font-weight-medium"
                                                                                    variant="primary"
                                                                                    type="button"
                                                                                    onClick={(e)=>approveData(value)}>Approve</Button>
                                                                            </td>
                                                                            <td className="col-md-1">
                                                                                <Button className="btn btn-block btn-primary col-md-12 font-weight-medium"
                                                                                    variant="primary"
                                                                                    type="button"
                                                                                    onClick={(e)=>rejectData(value)}>Reject</Button>
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