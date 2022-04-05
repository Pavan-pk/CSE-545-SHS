const { default: LoginComponent } = require("./Components/Login");
const { default: UserProfile } = require("./Components/PatientsComponent/UserProfile");
const { default: SignUp } = require("./Components/SignUp");
const { default: NotImplemented } = require("./Components/CommonComponents/NotImplemented");
const { default: Appointments } = require("./Components/PatientsComponent/Appointments");
const { default: Transactions } = require("./Components/PatientsComponent/Transactions");
const { default: MedicalRecords } = require("./Components/PatientsComponent/MedicalRecords");

const { default: adminProfile } = require("./Components/AdminComponents/AdminProfile.js");
const { default: ViewEditRecords } = require("./Components/ViewEditRecords");
const { default: PasswordReset } = require("./Components/PasswordReset");

const { default: DoctorProfile } = require("./Components/DoctorsComponent/DoctorProfile.js");
const { default: CreatePatientDiagnosis } = require("./Components/DoctorsComponent/CreatePatientDiagnosis");
const { default: PatientRecords } = require("./Components/DoctorsComponent/PatientRecords");

const { default: LabStaffProfile } = require("./Components/LabStaffComponent/LabStaffProfile.js");
const { default: LabTestReports } = require("./Components/LabStaffComponent/LabTestReports.js");
const { default: RudLabTestReports } = require("./Components/LabStaffComponent/RudLabTestReports.js");

const { default: InsuranceStaffProfile } = require("./Components/InsuranceComponent/InsuranceStaffProfile.js");
const { default: ManageInsurance } = require("./Components/InsuranceComponent/ManageInsurance.js");


const { default: HospitalStaffProfile } = require("./Components/HospitalStaffComponent/HospitalStaffProfile.js");
const { default: ManageDiagnosisRecords } = require("./Components/HospitalStaffComponent/ManageDiagnosisRecords.js");
const { default: CreatePatientRecords } = require("./Components/HospitalStaffComponent/CreatePatientRecords.js");
const { default: EditPatientRecords } = require("./Components/HospitalStaffComponent/EditPatientRecords.js");
const { default: ApproveAppointment } = require("./Components/HospitalStaffComponent/ApproveAppointment.js");
const { default: ApproveAccounts } = require("./Components/AdminComponents/AdminApproveUser.js")
const { default: AdminLogs } = require("./Components/AdminComponents/AdminLogs.js")
const { default: Records } = require("./Components/AdminComponents/Records")
const { default: PatientInsrance } = require("./Components/PatientsComponent/PatientInsurance")
const { default: EditLabRecords } = require("./Components/LabStaffComponent/EditLabRecords.js")
const { default: InitiateTransactions } = require("./Components/HospitalStaffComponent/Transactions.js")
const { default: ApproveTransactions } = require("./Components/AdminComponents/ApproveTransactions.js")
const { default: ChangeInsurancePatient } = require("./Components/InsuranceComponent/ChangeInsurancePaitent.js")


const routes = [
    {
      path:"/signup",
      component: SignUp,
      isPrivate: false
    },
    {
      path: "/patient/userprofile",
      component: UserProfile,
      isPrivate: true
    },
    {
      path: "/notimplemented",
      component: NotImplemented,
      isPrivate: true
    },
    {
      path: "/patient/appointments",
      component: Appointments,
      isPrivate: true

    },
    {
      path: "/patient/transactions",
      component: Transactions,
      isPrivate: true
    },
    {
      path: "/patient/medicalrecords",
      component: MedicalRecords,
      isPrivate: true
    },
    {
      path: "/patient/patientInsrance",
      component: PatientInsrance,
      isPrivate: true
    },
    {
      path: "/doctor/doctorprofile",
      component: DoctorProfile,
      isPrivate: true
    },
    {
      path: "/doctor/CreatePatientDiagnosis",
      component: CreatePatientDiagnosis,
      isPrivate: true
    },

    {
      path: "/doctor/PatientRecords",
      component: PatientRecords,
      isPrivate: true
    },

    {
      path: "/lab/LabStaffProfile",
      component: LabStaffProfile,
      isPrivate: true
    },

    {
      path: "/lab/LabTestReports",
      component: LabTestReports,
      isPrivate: true
    },

    {
      path: "/lab/RudLabTestReports",
      component: RudLabTestReports,
      isPrivate: true
    },
    {
      path: "/lab/editLabRecords",
      component: EditLabRecords,
      isPrivate: true
    },

    {
      path: "/insurance/InsuranceStaffProfile",
      component: InsuranceStaffProfile,
      isPrivate: true
    },

    {
      path: "/insurance/ManageInsurance",
      component: ManageInsurance,
      isPrivate: true
    },
    {
      path:"/insurance/changePolicy",
      component: ChangeInsurancePatient,
      isPrivate: true
    },
    {
      path: "/admin/adminProfile",
      component: adminProfile,
      isPrivate: true
    },
    {
      path: "/admin/records",
      component: Records,
      isPrivate: true
    },
    {
      path: "/admin/approveAccounts",
      component: ApproveAccounts,
      isPrivate: true
    },
    {
      path: "/admin/logs",
      component: AdminLogs,
      isPrivate: true
    },
    {
      path: "/admin/approveTransactions",
      component:ApproveTransactions,
      isPrivate: true
    },
    {
      path: "/viewEditRecords",
      component: ViewEditRecords,
      isPrivate: true,
    },

    {
      path: "/hospitalstaff/HospitalStaffProfile",
      component: HospitalStaffProfile,
      isPrivate: true,
    },

    {
      path: "/hospitalstaff/ManageDiagnosisRecords",
      component: ManageDiagnosisRecords,
      isPrivate: true,
    },
    {
      path: "/hospitalstaff/CreatePatientRecords",
      component: CreatePatientRecords,
      isPrivate: true,
    },
    {
      path: "/hospitalstaff/EditPatientRecords",
      component: EditPatientRecords,
      isPrivate: true,
    },
    {
      path: "/hospitalstaff/ApproveAppointment",
      component: ApproveAppointment,
      isPrivate: true,
    },
    {
      path: "/hospitalstaff/transactions",
      component: InitiateTransactions,
      isPrivate: true
    },
    {
      path: "/passwordreset",
      component: PasswordReset,
      isPrivate: false
    },
    {
      path: "/",
      component: LoginComponent,
      isPrivate: false,
    }
]

export default routes