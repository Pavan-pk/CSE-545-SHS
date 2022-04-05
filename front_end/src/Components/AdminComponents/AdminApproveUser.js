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
import {APPROVE_DENY_NEW_ACCOUNT, GET_NEW_ACCOUNT_APPROVE_LIST, REJECT_ACCOUNTS, USER_SEND_OTP} from "../../Constants/PathConstants";
import {SUCCESS} from "../../Constants/StringConstant"

export default function ApproveAccounts(props){
    const [accountList, setaccountList] = useState([])

    useEffect(()=> {
        setaccountLists()
    }, [])

    const setaccountLists = () => {
        HttpService.postFetch(GET_NEW_ACCOUNT_APPROVE_LIST, {})
        .then((responseData) => 
        {
            const response = JSON.parse(HttpService.decrypt(responseData.response))
            if (response.Status === SUCCESS){
                if(!!response.Data){
                    setaccountList(response.Data)
                } else {
                    setaccountList([])
                }
              } else {
                props.showAlertDialog(response.Message)
              }
        })
    }
    const approveData = (value) => {
        HttpService.postFetch(APPROVE_DENY_NEW_ACCOUNT, {"user_id":value.user_id, "approved":"Approved"})
        .then((responseData) => {
            const response = JSON.parse(HttpService.decrypt(responseData.response))
            if (response.Status === SUCCESS){
                setaccountLists()
              } else {
                props.showAlertDialog(response.Message)
            }
        })
    }

    const rejectData = (value) => {
        HttpService.postFetch(APPROVE_DENY_NEW_ACCOUNT, {"user_id":value.user_id, "approved":"Rejected"})
        .then((responseData) => {
            const response = JSON.parse(HttpService.decrypt(responseData.response))
            if (response.Status === SUCCESS){
                setaccountLists()
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
                    <h4 className="card-title">Accounts</h4>
                    {
                        accountList.length === 0  ?
                        <p className="card-description"> No accounts to approve. </p> :
                            (
                                <div>  
                                    {
                                        accountList.length !== 0 && (
                                            <div style={{marginTop:"3rem"}}>
                                              
                                                <div className='table-responsive'>
                                                    <table className='table'>
                                                        <thead>
                                                            <tr>
                                                                <th>Name</th>
                                                                <th>Email</th>
                                                                <th></th>
                                                                <th></th>
                                                            </tr>
                                                        </thead>
                                                        <tbody>
                                                            {
                                                                Object.entries(accountList).map(([key,value]) => {
                                                                    return (
                                                                        <tr>
                                                                            <td className="col-md-2">{value.full_name}</td>
                                                                            <td className="col-md-3">{value.email}</td>
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