/*
 * Copyright IBM Corp. All Rights Reserved.
 *
 * SPDX-License-Identifier: Apache-2.0
 */

'use strict';

const { Contract } = require('fabric-contract-api');

class FabCar extends Contract {

    async initLedger(ctx){    
        var transaction = {
            transaction_id: "T_ID",
            user_id: "USER_ID",
            birth_date: "BIRTH_DATE",
            email: "EMAIL",
            transaction_type: "T_TYPE",
            user_type: "U_TYPE",
            transaction_details: "{'T_DETAILS':'DETAILS'}"
        };
        await ctx.stub.putState(transaction.transaction_id, Buffer.from(JSON.stringify(transaction)));
        return "Initialization ledger successful";
    }

    async writeData(ctx, t_id, u_id, b_date, email_id, t_type, u_type, t_details){
        var transaction = {
            transaction_id: t_id,
            user_id: u_id,
            birth_date: b_date,
            email: email_id,
            transaction_type: t_type,
            user_type: u_type,
            transaction_details: t_details
        };
        await ctx.stub.putState(transaction.transaction_id, Buffer.from(JSON.stringify(transaction)));
        return JSON.stringify(transaction);
    }

    async readData(ctx){
        const startKey = '';
        const endKey = '';
        const allResults = [];
        for await (const {key, value} of ctx.stub.getStateByRange(startKey, endKey)) {
            const strValue = Buffer.from(value).toString('utf8');
            let record;
            try {
                record = JSON.parse(strValue);
            } catch (err) {
                console.log(err);
                record = strValue;
            }
            allResults.push({ Key: key, Record: record });
        }
        console.info(allResults);
        return JSON.stringify(allResults);
    }

    async readDataBy(ctx, field, field_value){
        const startKey = '';
        const endKey = '';
        const allResults = [];
        for await (const {key, value} of ctx.stub.getStateByRange(startKey, endKey)) {
            const strValue = Buffer.from(value).toString('utf8');
            let record;
            try {
                record = JSON.parse(strValue);
                if (record[field]!=field_value){
                    continue
                }
            } catch (err) {
                console.log(err);
                record = strValue;
            }
            allResults.push({ Key: key, Record: record });
        }
        console.info(allResults);
        return JSON.stringify(allResults);
    }

}

module.exports = FabCar;
