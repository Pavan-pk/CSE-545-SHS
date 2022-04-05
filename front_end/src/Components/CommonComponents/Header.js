import React, { Component } from 'react';
import { Dropdown } from 'react-bootstrap';
import { UserContext } from "../ContextProvider"




class Navbar extends Component {
  static contextType = UserContext;

  signout = event => {
    event.preventDefault();
    let logout = this.context.logout
    logout();
  }

  toggleOffcanvas() {
    document.querySelector('.sidebar-offcanvas').classList.toggle('active');
  }
  toggleRightSidebar() {
    document.querySelector('.right-sidebar').classList.toggle('open');
  }




  render () {  
    return (
      <nav className="navbar col-lg-12 col-12 p-lg-0 fixed-top d-flex flex-row">
        <div className="navbar-menu-wrapper d-flex align-items-center justify-content-between">
          <button className="navbar-toggler navbar-toggler align-self-center" type="button" onClick={ () => document.body.classList.toggle('sidebar-icon-only') }>
            <i className="mdi mdi-menu"></i>
          </button>
          <ul className="navbar-nav navbar-nav-right">
            <li className="nav-item  nav-profile border-0">
              <Dropdown>
                <Dropdown.Toggle className="nav-link count-indicator bg-transparent">
                    <i className="bi-person-circle"></i>
                </Dropdown.Toggle>
                <Dropdown.Menu className="navbar-dropdown preview-list">            
                  <Dropdown.Item className="dropdown-item preview-item d-flex align-items-center border-0" onClick={evt => this.signout(evt)}>
                    Sign Out
                  </Dropdown.Item>
                </Dropdown.Menu>
              </Dropdown>

            </li>
          </ul>
          <button className="navbar-toggler navbar-toggler-right d-lg-none align-self-center" type="button" onClick={this.toggleOffcanvas}>
            <span className="mdi mdi-menu"></span>
          </button>
        </div>
      </nav>
    );
  }
}

export default Navbar;
