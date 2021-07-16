
import React, { useState, useEffect } from "react";
import { Table, Button, Popconfirm, Input, message, Tooltip, Drawer } from "antd";
import AddAnomalyDef from "./AddAnomalyDef.js"
import EditAnomalyDef from "./EditAnomalyDef.js"
import RunStatus from "./RunStatus.js";
import { EditOutlined, DeleteOutlined, PlayCircleOutlined, CloseOutlined, EyeOutlined } from '@ant-design/icons';
import anomalyDefService from "services/anomalyDefinitions.js"
import scheduleService from "services/schedules"
import SelectSchedule from "components/Schedule/SelectSchedule"
import style from "./style.module.scss";


const { Search } = Input;
const ButtonGroup = Button.Group;
const granularity = {
  "day" : "Day",
  "hour" : "Hour",
  "week" : "Week"
 }

function anomalyDefName(record){
  let name = record.anomalyDef.metric + " " + (record.anomalyDef.dimension ? record.anomalyDef.dimension : "")
  name = name + (record.anomalyDef.top > 0 ? " Top " + record.anomalyDef.top : "")
  return name
}

let isTaskRunning = {}

export default function Connection() {
  const [data, setData] = useState();
  const [editAnomalyDef, setEditAnomalyDef] = useState([]);
  const [editAnomalyDefinition, setEditAnomalyDefinition] = useState(false);
  const [addAnomalyDef, setAddAnomalyDef] = useState(false);
  const [selectedAnomalyDef, setSelectedAnomalyDef] = useState();
  const [runStatusAnomalyDef, setRunStatusAnomalyDef] = useState();
  const [isRunStatusDrawerVisible, setIsRunStatusDrawerVisible] = useState(false);

  useEffect(() => {
    if (!data) {
        fetchData();
    }
  }, []);

  const fetchData = async () => {
    const response = await anomalyDefService.getAnomalyDefs();
    if(response){
      setData(response.data)
    }
  }

const getDeleteAnomalyDef = async (id) =>{
  const response = await anomalyDefService.deleteAnomalyDef(id)
  if(response.success){
    fetchData() // Refresh table
  }

}
const deleteAnomalyDef = (anomalyDef) =>{
  getDeleteAnomalyDef(anomalyDef.id)
  
}

const checkIsRunning = async (anomalyDefId) => {
  const response = await anomalyDefService.isTaskRunning(anomalyDefId)
  if(!response.isRunning)
  {
    clearInterval(isTaskRunning[anomalyDefId])
    delete isTaskRunning[anomalyDefId]
    fetchData()
  }
}

const runAnomalyDef = async (anomalyDef) => {
  const response = await anomalyDefService.runAnomalyDef(anomalyDef.id)
  isTaskRunning[anomalyDef.id] = setInterval(() => checkIsRunning(anomalyDef.id), 5000);
  fetchData()
}

const openRunStatus = (anomalyDef) => {
  setRunStatusAnomalyDef(anomalyDef)
  setIsRunStatusDrawerVisible(true)
}

const closeRunStatus = () => {
  setIsRunStatusDrawerVisible(false)
}

const addingAnomaly = (val) => {
  setAddAnomalyDef(val)
}

const editAnomlay = (anomalyDef) => {
  setEditAnomalyDefinition(true)
  setEditAnomalyDef(anomalyDef)
}
const onEditAnomalyDefSuccess = (val) => {
  if(val){
    fetchData() // Refresh table 
  }
  setEditAnomalyDefinition(!editAnomalyDefinition)
}

const onAddAnomalyDefSuccess = (val) =>{
  if(val){
    fetchData() // Refresh table 
  }
  setAddAnomalyDef(!addAnomalyDef)
}

const showScheduleDropDown = (anomalyDefId) => {
  setSelectedAnomalyDef(anomalyDefId)
}

const addAnomalyDefSchedule = async (selectedSchedule) => {
  if(selectedSchedule && selectedAnomalyDef && selectedSchedule !== -1){
    const response = await scheduleService.addAnomalyDefSchedule(selectedAnomalyDef, selectedSchedule);
    if(response.success){
      message.success(response.message)
    }
    else{
      message.error(response.message)
    }
    setSelectedAnomalyDef(null)
    fetchData()
  }
  else{
    alert('Schedule not selected')
  }
}
const unassignSchedule = async (anomalyDefId) => {
  const response = await scheduleService.unassignSchedule(anomalyDefId);
  if(response.success){
    fetchData()
  }
  else{
    message.error(response.message)
  }
}





  const columns = [    
      {
        title: "Dataset",
        dataIndex: "dataset",
        key: "datasetName",
        sorter:(a, b) =>   a.dataset.name.localeCompare(b.dataset.name),

        render: (text, record) => {
          return (
            <div>
              {record.dataset.name}
            </div>
          )
        }

      },
      {
        title: "Granularity",
        dataIndex: "granularity",
        key: "granularity",
        sorter:(a, b) => a && a.dataset.granularity &&  a.dataset.granularity.localeCompare(b.dataset.granularity),
        render: (text, record) => {
          return (
            <div>
              {granularity[record.dataset.granularity]}
            </div>
          )
        }
      },
      {
        title: "Anomaly Definition",
        dataIndex: "anomalyDef",
        key: "anomalyDef",
        sorter:(a, b) => parseInt(a.anomalyDef.top) - parseInt(b.anomalyDef.top),
        render:(text, record) => {
          return (         
                <div style={{fontSize:14}}>
                 <span style={{color: "#4B0082"}}> {record.anomalyDef.metric}</span>
                  <span style={{color: "#12b1ff"}}> {record.anomalyDef.dimension ? record.anomalyDef.dimension : null}</span>
                  <span style={{color: "#ff6767"}}> {record.anomalyDef.top > 0 ? "Top " + record.anomalyDef.top : null}</span>
                  <span style={{color: "#02c1a3"}}> {record.anomalyDef.highOrLow}</span>
                  </div>

              )
      
        }

      },
      {
        title: "Schedule",
        dataIndex: "schedule",
        key: "schedule",
        render: (schedule, record) => {
          if(schedule && selectedAnomalyDef != record.id){
            return (
              <>
              <div className={style.scheduleText}>
                <span>{schedule}</span>
                <Tooltip title={"Unassign Schedule"}> 
                  <span className={style.icon} onClick={()=>unassignSchedule(record.id)}><CloseOutlined /></span>
                </Tooltip>
              </div>
              </>
            )
          }
          else{
            return (
              <>
                { 
  
                  selectedAnomalyDef == record.id ?
                  <SelectSchedule onChange={addAnomalyDefSchedule} />
                  :
                  <a className={style.linkText} onClick={()=>showScheduleDropDown(record.id)}>Assign Schedule</a>
                }
              </>
            );
          }
        }

      },
      {
        title: "Last Run",
        dataIndex: "lastRun",
        key: "lastRun",

      },
      {
        title: "Last Run Status",
        dataIndex: "lastRunStatus",
        key: "lastRunStatus",

      },
      {
        title: "Last Run Anomalies",
        dataIndex: "lastRunAnomaly",
        key: "lastRunAnomaly",

      },
      {
        title: "",
        dataIndex: "",
        key: "",
        render: (text, record) => (
         <div className={style.actions}>
           {isTaskRunning[record.id]?(<Tooltip title={"Anomaly Detection Running"}>
              <PlayCircleOutlined style={{opacity: 0.3}}/>
            </Tooltip>):(<Tooltip title={"Run Anomaly Detection"}>
              <PlayCircleOutlined onClick={()=> runAnomalyDef(record)} />
            </Tooltip>)}

           <Tooltip title={"View Anomaly Detection Runs"}>
              <EyeOutlined onClick={() => openRunStatus(record)} />
            </Tooltip>
           <Tooltip title={"Edit Anomaly Definition"}>
              <EditOutlined onClick={() => editAnomlay(record)} />
            </Tooltip>
            <Popconfirm
                title={"Are you sure to delete "+ anomalyDefName(record) +"?"}
                onConfirm={() => deleteAnomalyDef(record)}
                okText="Yes"
                cancelText="No"
            >
                <Tooltip title={"Delete Anomaly Definition"}>
                    <DeleteOutlined />
                </Tooltip>
            </Popconfirm>
          </div>
        )
      }
    ];
    return (
      <div>
        <div className={`d-flex flex-column justify-content-center text-right mb-2`}>
        <Button
            type="primary"
            onClick={() => addingAnomaly(true)}
          >
            Add Anomaly Definition
          </Button>
          
        </div>
        <Table
            rowKey={"id"}
            scroll={{ x: "100%" }}
            columns={columns}
            dataSource={data}
            size={"small"}
            pagination={{
              pageSize:20,
              total:  data ? data.length : 20
            }}
            
        />
        {
          addAnomalyDef ? 
          <AddAnomalyDef onAddAnomalyDefSuccess={onAddAnomalyDefSuccess}  />
          : null
        }
        {
          editAnomalyDefinition ? 
          <EditAnomalyDef onEditAnomalyDefSuccess={onEditAnomalyDefSuccess} editAnomalyDef={editAnomalyDef}/> 
          : null
        }
      <Drawer
          title={"Anomaly Detection Runs"}
          width={720}
          onClose={closeRunStatus}
          visible={isRunStatusDrawerVisible}
          bodyStyle={{ paddingBottom: 80 }}
          footer={
            <div
              style={{
                textAlign: 'right',
              }}
            >
              <Button onClick={closeRunStatus} style={{ marginRight: 8 }}>
                Close
              </Button>
            </div>
          }
        >
          { isRunStatusDrawerVisible 
            ? 
            <RunStatus anomalyDef={runStatusAnomalyDef}></RunStatus>
            :
            null
          }
      </Drawer>
      </div>
    );
  }