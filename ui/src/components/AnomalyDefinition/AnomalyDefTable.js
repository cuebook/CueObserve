
import React, { useState, useEffect, useRef } from "react";
import { Table, Button, Popconfirm, Input, message, Tooltip, Drawer, Modal } from "antd";

import AddAnomalyDef from "./AddAnomalyDef.js"
import EditAnomalyDef from "./EditAnomalyDef.js"
import RunStatus from "./RunStatus.js";
import RunStatusAnomalies from "./RunStatusAnomalies.js";
import { EditOutlined, DeleteOutlined, PlayCircleOutlined, CloseOutlined, EyeOutlined } from '@ant-design/icons';
import anomalyDefService from "services/anomalyDefinitions.js"
import scheduleService from "services/schedules"
import SelectSchedule from "components/Schedule/SelectSchedule"
import style from "./style.module.scss";
// import { search } from "services/general.js"


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
  const [searchText, setSearchText] = useState("");
  const [latestAnomaliesRunStatusId, setLatestAnomaliesRunStatusId] = useState();
  const [latestAnomaliesModalVisibile, setLatestAnomaliesModalVisibile] = useState(false);
  const [limit] = useState(50)
  const [total, setTotal] = useState(0) 
  const [currentPage, setCurrentPage] = useState(1);
  const [sorter, setSorter] = useState({})
  const currentPageRef = useRef(currentPage);
  currentPageRef.current = currentPage;
  const sorterRef = useRef(sorter);
  sorterRef.current = sorter;
  const searchTextRef = useRef(searchText);
  searchTextRef.current = searchText;
  useEffect(() => {
    if (!data) {
        fetchData();
    }
  }, []);

  const fetchData = async (currentPage = currentPageRef.current, searchText = searchTextRef.current, sorter = sorterRef.current) => {
    const response = await anomalyDefService.getAnomalyDefs((currentPage -1)*limit, limit, searchText, sorter);
    if(response && response.data){
      setData(response.data.anomalyDefinition)
      setTotal(response.data.count)
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

const openLatestAnomalies = (runStatusId) => {
  setLatestAnomaliesRunStatusId(runStatusId)
  setLatestAnomaliesModalVisibile(true)
}

const closeLatestAnomalies = () => {
  setLatestAnomaliesModalVisibile(false)
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
const handleTableChange = (event, filter, sorter) => {
  setCurrentPage(event.current)
  setSorter({"columnKey":sorter.columnKey, "order":sorter.order})
  fetchData(event.current, searchText,{"columnKey":sorter.columnKey, "order":sorter.order})
}



const searchInAnomalyDef = (val) =>{
  setSearchText(val)
  setCurrentPage(1)
  fetchData(1, val, sorter)
}

  const columns = [    
      {
        title: "Dataset",
        dataIndex: "datasetName",
        key: "datasetName",
        sorter:(a, b) =>   {},

        render: (text, record) => {
          return (
            <div>
              {record.datasetName}
            </div>
          )
        }

      },
      {
        title: "Granularity",
        dataIndex: "datasetGranularity",
        key: "granularity",
        sorter:(a, b) => {},
        render: (text, record) => {
          return (
            <div>
              {granularity[record.datasetGranularity]}
            </div>
          )
        }
      },
      {
        title: "Anomaly Definition",
        dataIndex: "anomalyDef",
        key: "anomalyDef",
        sorter:(a, b) => {},
        render:(text, record) => {
          return (         
                <div style={{fontSize:14}}>
                 <span style={{color: "#4B0082"}}> {record.anomalyDef.metric}</span>
                  <span style={{color: "#12b1ff"}}> {record.anomalyDef.dimension ? record.anomalyDef.dimension : null}</span>
                  <span style={{color: "#12b1ff"}}> {record.anomalyDef.value > 0 ? record.anomalyDef.operation +" " + record.anomalyDef.value : null}</span>
                  <span style={{color: "#02c1a3"}}> {record.anomalyDef.highOrLow}</span>
                  <div><span style={{color: "#929292"}}> {record.detectionRule.detectionRuleStr}</span></div>
                  </div>

              )
      
        }

      },
      {
        title: "Schedule",
        dataIndex: "schedule",
        key: "schedule",
        // sorter:(a, b) =>  {}, Will implement in future if needed
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
        sorter: (a, b) =>{},

      },
      {
        title: "Last Run Status",
        dataIndex: "lastRunStatus",
        key: "lastRunStatus",
        sorter: (a, b) => {},

      },
      {
        title: "Last Run Anomalies",
        dataIndex: "lastRunAnomalies",
        key: "lastRunAnomalies",
        // sorter: (a, b) => {}, Will implement in future if needed
        render: (text, record) => {
          return (
            <span>
              <a className={style.linkText} onClick={()=> openLatestAnomalies(record.lastRunAnomalies.runStatusId)}>
              { record.lastRunAnomalies && record.lastRunAnomalies.numAnomaliesPulished} {record.lastRunAnomalies && record.lastRunAnomalies.numAnomalySubtasks?("("+record.lastRunAnomalies.numAnomalySubtasks+")"):""} 
              </a>
            </span>
          );
        }

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

        <Search
                style={{ margin: "0 0 10px 0" , width:350, float: "left"}}
                placeholder="Search"
                enterButton="Search"
                onSearch={e=>searchInAnomalyDef(e)}
                className="mr-2"
              />
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
            onChange={handleTableChange}
            pagination={{

              showSizeChanger: false,
              current: currentPage,
              pageSize : limit,
              total : data ? total : 50
            }}
            size={"small"}
            
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
      <Modal 
          title="Last Run Anomalies"
          visible={latestAnomaliesModalVisibile}
          onCancel={closeLatestAnomalies}
          onOk={closeLatestAnomalies}
        >
          {
            latestAnomaliesModalVisibile ? <RunStatusAnomalies runStatusId={latestAnomaliesRunStatusId} /> : null
          }
        </Modal>
      </div>
    );
  }