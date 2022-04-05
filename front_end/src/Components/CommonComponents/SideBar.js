import React, { useState, useEffect } from 'react';
import { Link, useLocation } from 'react-router-dom';
import icon from '../../assets/images/icon.png'
import { UserContext } from "../ContextProvider"


export default function Sidebar(props){
    const [currPath, setCurrPath] = useState("")
    const [options, setOption] = useState({})
    const {username, usertype} = React.useContext(UserContext);
    const location = useLocation()
    const isPathActive = (path) => {
        return location.pathname.startsWith(path)
      }

    const patientPathDict = {
        "Profile": "/patient/userprofile",
        "Update Insurace Info": "/patient/patientInsrance",
        "Book Appointments": "/patient/appointments",
        "Transaction": "/patient/transactions",
        "Medical Records": "/patient/medicalrecords",}

    const doctorPathDict = {
        "Profile": "/doctor/doctorprofile",
        "Create Patient Diagnosis": "/doctor/createPatientDiagnosis",
        "Records": "/doctor/patientRecords",
    }

    const hospitalstaffPathDict = {
        "Profile": "/hospitalstaff/hospitalStaffProfile",
        "Appointments": "/hospitalstaff/approveAppointment",
        "Create Patient Info": "/hospitalstaff/createPatientRecords",
        "Edit Patient Info": "/hospitalstaff/editPatientRecords",
        "View Patient Records": "/hospitalstaff/manageDiagnosisRecords",
        "Transactions": "/hospitalstaff/transactions",
    }

    const labstaffPathDict = {
        "Profile": "/lab/labStaffProfile",
        "Create lab tests": "/lab/labTestReports",
        "View all reports": "/lab/rudLabTestReports",
        "Edit records":"/lab/editLabRecords"
    }

    const insurancestaffPathDict = {
        "Profile": "/insurance/InsuranceStaffProfile",
       // "Insurance Policy": "/insurance/policy",
        "Insurance Request": "/insurance/ManageInsurance",
        "Edit Patient Insurance Policy": "/insurance/changePolicy"
    }

    const adminStaffPathDict = {
        "Admin": "/admin/adminProfile",
        "Delete Records": "/admin/records",
        "Approve Accounts": "/admin/approveAccounts",
        "Approve Transactions": "/admin/approveTransactions",
        "Operations Logs": "/admin/logs"
    }

    const toggleState = (path) => {
        if(getOptions()[path] === currPath){
            setCurrPath("")
        } else {
            setCurrPath(getOptions()[path])
        }
    }

    const resetRoutes = () => {
        setCurrPath("")
    }

    const getOptions = () => {
        let ret_val = {}
        switch(usertype){
            case "1": 
                ret_val = patientPathDict;
                break;
            case "2":
                ret_val = hospitalstaffPathDict;
                break;
            case "3":
                ret_val = doctorPathDict;
                break;
            case "4":
                ret_val = labstaffPathDict;
                break;
            case "5":
                ret_val = insurancestaffPathDict;
                break;
            case "6":
                ret_val = adminStaffPathDict;
        }
        return ret_val
    }

    const onRouteChanged = () => {
        document.querySelector('#sidebar').classList.remove('active');
        resetRoutes()
        for (const [key, value] of Object.entries(getOptions())){
            if (isPathActive(value)){
                setCurrPath(location.pathname)
            }
        }
    }

    const getUserType = () => {
        let ret_val = ""
        switch(usertype){
            case "1": 
                ret_val = "Patient";
                break;
            case "2": 
                ret_val = "Hospital Staff";
                break;
            case "3":
                ret_val = "Doctor";
                break;
            case "4": 
                ret_val = "Lab Staff";
                break;
            case "5": 
                ret_val = "Insurance Satff";
                break
            case "6": 
                ret_val = "Admin";
        }
        return ret_val
    }

    useEffect(() => {
        onRouteChanged();
        // add className 'hover-open' to sidebar navitem while hover in sidebar-icon-only menu
        const body = document.querySelector('body');
        document.querySelectorAll('.sidebar .nav-item').forEach((el) => {
          el.addEventListener('mouseover', function() {
            if(body.classList.contains('sidebar-icon-only')) {
              el.classList.add('hover-open');
            }
          });
          el.addEventListener('mouseout', function() {
            if(body.classList.contains('sidebar-icon-only')) {
              el.classList.remove('hover-open');
            }
          });
        });
        setOption(getOptions())
    }, [usertype])

    return(
        <nav className="sidebar sidebar-offcanvas" id="sidebar">
            <div className="text-center sidebar-brand-wrapper d-flex align-items-center">
            <a className="sidebar-brand brand-logo" style={{width:"50px"}}><img src={icon} alt="logo" /></a>
            </div>
            <ul className="nav">
            <li className="nav-item nav-profile not-navigation-link">
                <div className="nav-link">
                    <div className="d-flex justify-content-between align-items-start">
                    <div className="text-wrapper">
                        <p className="profile-name">{username}</p>
                        <p className="designation">{getUserType()}</p>
                    </div> 
                    </div>
                </div>
            </li> 
            {
                Object.entries(options).map(([key, value]) => {
                    return (
                    <li className={isPathActive(value) ? 'nav-item active' : 'nav-item' } key={key}>
                        <Link className="nav-link" to={value}>
                        <i className="mdi mdi-television menu-icon"></i>
                        <span className="menu-title">{key}</span>
                    </Link>
                </li>)
                })
            }
            </ul>
        </nav>
    )
}