import React, { useContext, useEffect, useState, useRef } from 'react';
import './App.scss';
import { Navigate, useLocation } from 'react-router-dom';
import {UserContext} from './Components/ContextProvider';
import Header from "./Components/CommonComponents/Header";
import Sidebar from './Components/CommonComponents/SideBar';
import Footer from './Components/CommonComponents/Footer';
import { Alert } from 'react-bootstrap';

import Header1 from "./Components/ChatBot/components/Header";
import BotMessage from "./Components/ChatBot/components/BotMessage";
import UserMessage from "./Components/ChatBot/components/UserMessage";
import Messages from "./Components/ChatBot/components/Messages";
import Input from "./Components/ChatBot/components/Input";
import API from "./Components/ChatBot/ChatBotAPI";
import Fab from '@mui/material/Fab';
import MessageIcon from '@mui/icons-material/Message';

const AppRouter = (props) => {

  const [messages, setMessages] = useState([]);
  const {userTypeString} = React.useContext(UserContext);

  const [display, toggleDisplay] = useState(false)

  useEffect(() => {
    async function loadWelcomeMessage() {
      setMessages([
        <BotMessage
          key="0"
          fetchMessage={async () => await API.GetChatbotResponse("", "hi")}
        />
      ]);
    }
    loadWelcomeMessage();
  }, []);

  const send = async (text) => {
    const newMessages = messages.concat(
      <UserMessage key={messages.length + 1} text={text} />,
      <BotMessage
        key={messages.length + 2}
        fetchMessage={async () => await API.GetChatbotResponse(userTypeString,text)}
      />
    );
    setMessages(newMessages);
  };

  const [show, setShow] = useState(false);
  const target = useRef(null);


  const { auth } = useContext(UserContext);
  const [isFullPageLayout, setPageLayout] = useState(false)
  const [showAlert, setShowAlert] = useState(false)
  const [alertMsg, setAlertMsg] = useState('')
  const location = useLocation()
  const fullPageLayouts = ["/", "/signup", "/passwordreset"]
  useEffect(() => {
      if (fullPageLayouts.includes(location.pathname)){
        setPageLayout(true);
      } else {
        setPageLayout(false)
      }
    }, [location.pathname])
  if (!auth && props.isPrivate) {
    // pathname will be location.
    return <Navigate to="/" state={{ from: location.pathname }} replace />;
  }
  const children = props.children;
  const showAlertDialog = (msg) => {
    setAlertMsg(msg)
    setShowAlert(true)
    setTimeout(()=>setShowAlert(false), 3000)
  }

  return isFullPageLayout ? children : (
    <div className="container-scroller">
      <div style={{position:"absolute", top:"0.5rem", right:"6rem", top:"0.7rem"}}>
        <Fab variant="extended" color="primary" style={{marginLeft:"30rem"}, {height: 37}} aria-label="chat"  ref={target} onClick={() => setShow(!show)}>
          <MessageIcon sx={{mr:1}}/>
          Chat Help
        </Fab> 
        <div style={{position:"absolute", top:"3.3rem", right:"0rem", zIndex:"15", display:show?"block":"none"}} className="chatbot" >
                      <Header1/>
                      <Messages messages={messages} />
                      <Input onSend={send} />
        </div>
        <Header/>
      </div>
      <div className="container-fluid page-body-wrapper">
        <Sidebar />
        <div className="main-panel">
          <div className="content-wrapper">
            {React.cloneElement(children, {...children.props, showAlertDialog})}
          </div>
        </div>
      </div>
      <Alert show={showAlert} variant='danger' style={{"position":"sticky", "bottom":"1rem", "width":"100%"}}>
            <span style={{color:"red", fontWeight:"bolder"}}>{alertMsg}</span>
      </Alert>
      <Footer />
  </div>
  )
}

export default AppRouter