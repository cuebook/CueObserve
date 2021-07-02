
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

export default function Connection() {
  const [data, setData] = useState([]);
  const [editAnomalyDef, setEditAnomalyDef] = useState([]);
  const [edit, setEdit] = useState(false);

  useEffect(() => {
    if (!data.length) {
        fetchData();
    }
  }, []);

  const fetchData = async () => {
    const response = await anomalyDefService.getAnomalyDefs();
    setData(response.data)
  }


const deleteAnomalyDef = (anomalyDef) =>{
  const response = anomalyDefService.deleteAnomalyDef(anomalyDef.id)
}

const editAnomlay = (anomalyDef) => {
  setEdit(true)
  setEditAnomalyDef(anomalyDef)
}
const onEditAnomalyDefSuccess = (val) => {
  setEdit(val)
}

  const columns = [
      
      {
        title: "Dataset",
        dataIndex: "dataset",
        key: "dataset",
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
        render: (text, record) => {
          return (
            <div>
              {record.dataset.granularity}
            </div>
          )
        }
      },
      {
        title: "Anomaly Definition",
        dataIndex: "anomalyDef",
        key: "anomalyDef",
        render:(text, record) => {
          return (         
                <div style={{fontSize:14}}>
                 <span style={{color: "#ffc71f"}}> {record.anomalyDef.metric}</span>
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
        title: "Last Run Anomaly",
        dataIndex: "lastRunAnomaly",
        key: "lastRunAnomaly",

      },
      {
        title: "",
        dataIndex: "",
        key: "",
        render: (text, record) => (
         <div className={style.actions}>
           <Tooltip title={"Edit AnomalyDefinition"}>
              <EditOutlined onClick={() => editAnomlay(record)} />
            </Tooltip>
            <Popconfirm
                title={"Are you sure to delete Anomaly of id "+ record.id +"?"}
                onConfirm={() => deleteAnomalyDef(record)}
                // onCancel={cancel}
                okText="Yes"
                cancelText="No"
            >
                <Tooltip title={"Delete AnomalyDefinition"}>
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

            <ErrorBoundary>
              <AddAnomalyDef />
            </ErrorBoundary>
          {edit ? 
          <EditAnomalyDef onEditAnomalyDefSuccess={onEditAnomalyDefSuccess} editAnomalyDef={editAnomalyDef}/> 
          : null }
        </div>
        <Table
            rowKey={"id"}
            scroll={{ x: "100%" }}
            columns={columns}
            dataSource={data}
            pagination={false}
        />
           </div>
    );
  }