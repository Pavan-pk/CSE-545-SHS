import React, { useEffect, useState } from 'react';
import { Form, Button, input } from 'react-bootstrap';
import { UserContext } from "./ContextProvider";
import { useLocation } from 'react-router-dom';

export default function ViewEditRecords(props) {
  const location = useLocation()
  const edit = location.state.edit
  const [record, updateRecord] = useState(location.state.record)
  const [newKey, updateKey] = useState('');
  const [newDesc, updateDesc] = useState('')
  const onAdd = (event) => {
      event.preventDefault();
      updateRecord({
        ...record,
        [newKey]: newDesc,
      })
      updateKey('');
      updateDesc('');
  }
  const onSubmit = (event) => {
    event.preventDefault();
    //   request update on object here. {use record}
  }
  return(
        <div className="row">
            <div className="col-lg-12 grid-margin stretch-card">
                <div className="card">
                    <div className="card-body">
                    <h4 className="card-title">Records</h4>
                    {
                        (
                            <div>
                                <div style={{marginTop:"3rem"}}>
                                    <h4 className="card-title">Operation Records</h4>
                                    <div className='table-responsive'>
                                        <table className='table'>
                                            <tbody>
                                                {
                                                    Object.entries(record).map(([key, value]) => {
                                                        return (
                                                                <tr>
                                                                    <td>{key}</td>
                                                                    <td>
                                                                        <div className="col-sm-8" style={{height:'min-content'}}>
                                                                            <Form.Control type="text" value={value} onChange={(e) => record[key] = e.target.value} disabled={!edit}/>
                                                                        </div>
                                                                    </td>
                                                                    <td></td>
                                                                </tr>
                                                        )
                                                    })
                                                }
                                                { edit?
                                                    (<tr>
                                                        <td>
                                                            <div className="col-md-12">
                                                                <form className="ml-auto search-form d-none d-md-block" action="#">
                                                                    <div className="form-group col-sm-8">
                                                                        <input type="text" className="form-control" placeholder="Record Key" value={newKey} onChange={(e) => updateKey(e.target.value)}/>
                                                                    </div>
                                                                </form>
                                                            </div>
                                                        </td>
                                                        <td>
                                                            <div className="col-md-12">
                                                                <form className="ml-auto search-form d-none d-md-block" action="#">
                                                                    <div className="form-group col-sm-8">
                                                                        <input type="text" className="form-control" placeholder="Description" value={newDesc} onChange={(e) => updateDesc(e.target.value)} />
                                                                    </div>
                                                                </form>
                                                            </div>
                                                        </td>
                                                        <td>
                                                            <div className="row col-sm-6 d-flex flex-column">
                                                                <Button className="btn btn-block btn-primary btn-md font-weight-small auth-form-btn"
                                                                        variant="primary" type="submit" onClick={onAdd}>ADD</Button>
                                                            </div>
                                                        </td>
                                                    </tr>):(<div></div>)
                                                }
                                            </tbody>
                                        </table>
                                    </div>
                                </div>
                            </div>
                        )
                    }
                    {edit ?
                    (<div className="row col-md-2 mt-4 d-flex flex-column">
                        <Button className="btn btn-block btn-primary btn-md font-weight-medium auth-form-btn" variant="primary" type="submit">SUBMIT</Button>
                    </div>):(<div></div>)
                    }
                    </div>
                </div>
            </div>
        </div>                
  );
}
