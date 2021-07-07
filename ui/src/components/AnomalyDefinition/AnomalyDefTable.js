
import React, { useState, useEffect } from "react";
import { Table, Button, Popconfirm, Input, message, Tooltip, Drawer } from "antd";
import style from "./style.module.scss";
import AddAnomalyDef from "./AddAnomalyDef.js"
import EditAnomalyDef from "./EditAnomalyDef.js"
import { EditOutlined, DeleteOutlined } from '@ant-design/icons';
import ErrorBoundary from "antd/lib/alert/ErrorBoundary";
import anomalyDefService from "services/anomalyDefinitions.js"

const { Search } = Input;
const ButtonGroup = Button.Group;
const granularity = {
  "day" : "Day",
  "hour" : "Hour",
  "week" : "Week"
 }
export default function Connection() {
  const [data, setData] = useState();
  const [editAnomalyDef, setEditAnomalyDef] = useState([]);
  const [editAnomalyDefinition, setEditAnomalyDefinition] = useState(false);
  const [addAnomalyDef, setAddAnomalyDef] = useState(false);

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
        dataIndex: "shedule",
        key: "shedule",

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
           <Tooltip title={"Edit Anomaly Definition"}>
              <EditOutlined onClick={() => editAnomlay(record)} />
            </Tooltip>
            <Popconfirm
                title={"Are you sure to delete Anomaly of id "+ record.id +"?"}
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
      </div>
    );
  }