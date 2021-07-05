import React, { useState, useEffect, useRef } from "react";
import TimeAgo from 'react-timeago';
import _ from "lodash";
import datasetService from "services/datasets";
import style from "./style.module.scss";
import { useHistory } from "react-router-dom";
import {
  Table,
  Button,
  Popconfirm,
  Tooltip
} from "antd";
import { DeleteOutlined, EyeOutlined } from '@ant-design/icons';
import PopconfirmButton from "components/Utils/PopconfirmButton";

export default function DatasetsTable(props) {
  const [datasets, setDatasets] = useState(null);
  const history = useHistory();

  useEffect(()=>{
    if (!datasets){
      getDatasets();
    }
  }, []);

  const getDatasets = async () => {
    const data = await datasetService.getDatasets()
    if (data && data.length){
      setDatasets(data);
    }
  }

  const deleteDataset = async (record) => {
    const response = await datasetService.deleteDataset(record.id)
    if (response){
      getDatasets()
    }
  }

  const editDataset = record => {
    history.push('/dataset/' + record.id)
  }

  const createDataset = () => {
    history.push("/dataset/create")
  }

  const columns = [
    {
      title: "Datasets",
      dataIndex: "name",
      key: "name",
      sorter: (a, b) => a.name.localeCompare(b.name),
      render: text => {
        return (
          <p>{text}</p>
        );
      }
    },
    {
      title: "Connection",
      dataIndex: "connection",
      key: "connection",
      sorter: (a, b) => a.connection.name.localeCompare(b.connection.name),
      render: connection => {
        return (
          <p>{connection.name}</p>
        );
      }
    },
    {
      title: "Anomaly Definitions",
      dataIndex: "anomalyDefinitionCount",
      key: "anomalyDefinitionCount",
      sorter: (a, b) => a.anomalyDefinitionCount - b.anomalyDefinitionCount,
    },
    {
      title: "",
      dataIndex: "action",
      key: "actions",
      className: "text-right",
      render: (text, record) => {
        return (
          <div className={style.actions}>
             <Tooltip title={"View Dataset"}>
                 <EyeOutlined onClick={()=>editDataset(record)} />
             </Tooltip>

             <Popconfirm
                 title={"Are you sure to delete '"+ record.name +"'?"}
                 onConfirm={() => deleteDataset(record)}
                 // onCancel={cancel}
                 okText="Yes"
                 cancelText="No"
             >
                 <Tooltip title={"Delete Dataset"}>
                     <DeleteOutlined />
                 </Tooltip>
             </Popconfirm>
           </div>
        );
      }

    } 
  ]

  return (
    <div>
      <div style={{float: "right", paddingBottom: "5px"}}>
        <Button onClick={createDataset} type="primary">New Dataset</Button>
      </div>
      <Table
        rowKey={"id"}
        scroll={{ x: "100%" }}
        columns={columns}
        dataSource={datasets}
        size={"small"}
      />
    </div>
  )

}
