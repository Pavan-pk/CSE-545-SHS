import {createContext, useState, useContext, useMemo, useEffect } from 'react';
import { USER_LOGOUT } from '../Constants/PathConstants';
import HttpService from "../Services/HttpService";

export const UserContext = createContext();

export function UserContextProvider({children}){
    const [auth, setAuth] = useState(false);
    const [token, setToken] = useState('');
    const [username, setUserName] = useState('');
    const [usertype, setUserType] = useState('1')
    const [userid, setUserId] = useState('')
    const [userContact, setUserContact] = useState('')
    const [userEmail, setUserEmail] = useState('')
    const [userDob, setUserDob] = useState('1970-01-01')
    const [userGender, setUserGender] = useState('0')
    const [userTypeString, setUserTypeString] = useState('')
    const [userSpeciality, setUserSpeciality] = useState('')
    const [insuranceid, setInsuranceId] = useState('')

    useEffect(() => {
        return () => {
            logout()
        }
    }, []);

    const getUserType = () => {
        let ret_val = ""
        switch(usertype){
            case "1": 
                ret_val = "patient";
                break;
            case "2": 
                ret_val = "hospital staff";
                break;
            case "3":
                ret_val = "doctor";
                break;
            case "4": 
                ret_val = "lab staff";
                break;
            case "5": 
                ret_val = "insurance staff";
                break
            case "6": 
                ret_val = "administrator";
        }
        return ret_val
    }

    const login = userDetails => {
        // validate User
        setAuth(true)
        // email
        setUserEmail(userDetails.email)
        // userType
        setUserType(userDetails.user_type)
        if (userDetails.user_type === "3"){
            setUserSpeciality(userDetails.user_speciality)
        }
        setUserTypeString(getUserType(userDetails.user_type))
        setUserName(userDetails.full_name)
        setUserDob(userDetails.dob)
        setUserId(userDetails.user_id)
    }

    const setHttpToken = token => {
        setToken(token)
        HttpService.setToken(token)
    }

    const updateInfo = userDetails => {
        setUserDob(userDetails.dob)
        setUserName(userDetails.full_name)
        setInsuranceId(userDetails.insuranceId)
    }

    const logout = () => {
        HttpService.postFetch(USER_LOGOUT, {})
        // reset token
        setToken('')
        // reset Auth
        setAuth(false)
        // reset clientID
        setUserId('')
        // validate User

    }

    const value = {auth,
                    token,
                    username,
                    userid,
                    usertype,
                    userContact,
                    userEmail,
                    userDob,
                    userGender,
                    userTypeString,
                    userSpeciality,
                    insuranceid,
                    login, logout, setHttpToken, updateInfo}
    return (
        <UserContext.Provider value={value}>
         {children}
        </UserContext.Provider>
    );
  }