import React, { useState, useEffect } from 'react';
import { Form, Button, input, table } from 'react-bootstrap';
import { GET_TRANSACTIONS } from '../../Constants/PathConstants';
import { SUCCESS } from '../../Constants/StringConstant';
import HttpService from '../../Services/HttpService';
import { UserContext } from "../ContextProvider";

export default function Transactions(props){
    const {userid} = React.useContext(UserContext);
    const [transactionData, setTransactionData] = useState([])

    useEffect(()=>{
        getTransactions()
    },[])

    const getTransactions = () => {
        HttpService.postFetch(GET_TRANSACTIONS, {"user_id":userid})
        .then((responseData) => {
            const response = JSON.parse(HttpService.decrypt(responseData.response))
            if (response.Status === SUCCESS){
                setTransactionData(response.Data)
                props.showAlertDialog(response.Message)
            } else {
                props.showAlertDialog(response.Message)
            }
        })
    }
    // Ideally should get it when mounted in useEffect
    return(
        <div className="row">
            <div className="col-lg-12 grid-margin stretch-card">
                <div className="card">
                    <div className="card-body">
                    <h4 className="card-title">Transactions</h4>
                    <div className="table-responsive">
                        <table className="table">
                        <thead>
                            <tr>
                            <th>Transaction ID</th>
                            <th>Appointment ID</th>
                            <th>Description</th>
                            <th>Amount</th>
                            <th>Paid By</th>
                            <th>Transaction Status</th>
                            </tr>
                        </thead>
                        <tbody>
                            {
                                Object.entries(transactionData).map(([key, value]) => {
                                    return (
                                    <tr>
                                        <td className="col-md-2">{value.transaction_id}</td>
                                        <td className="col-md-2">{value.appointment_id}</td>
                                        <td className="col-md-2">{value.reason}</td>
                                        <td className="col-md-4">{value.transaction_amount}</td>
                                        <td className="col-md-2">{value.transaction_type}</td>
                                        <td className="col-md-3">{value.status}</td>
                                    </tr>
                                    )
                                })
                            }
                        </tbody>
                        </table>
                    </div>
                    </div>
                </div>
            </div>
        </div>);
};