import React, { useState, useEffect, useRef } from "react";
import TimeAgo from 'react-timeago';
import _ from "lodash";
import datasetService from "services/datasets";
import style from "./style.module.scss";
import { useHistory } from "react-router-dom";
import {
  Table,
  Button,
} from "antd";
import { MoreOutlined, PlayCircleOutlined, UnorderedListOutlined, StopOutlined, FileTextOutlined, DeleteOutlined, CopyOutlined, CloseOutlined, EditOutlined } from '@ant-design/icons';
import PopconfirmButton from "components/Utils/PopconfirmButton";

export default function DatasetsTable(props) {
  const [data, setData] = useState([]);
  const history = useHistory();

  useEffect(()=>{
    if (!data.length){
      getDatasets();
    }
  }, []);

  const getDatasets = async () => {
    const data = await datasetService.getDatasets()
    if (data && data.length){
      setData(data);
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
      sorter: ()=>{},
      ellipsis: true,

      render: text => {
        return (
          <p>{text}</p>
        );
      }
    },
    {
      title: "",
      dataIndex: "action",
      key: "actions",
      className: "text-right",
      sorter: ()=>{},
      ellipsis: true,

      render: (text, record) => {
        return (
          <div>
            <Button
              icon={<EditOutlined/>}
              onClick={() => editDataset(record)}
            >
              Edit
            </Button>
            <PopconfirmButton
              icon={<DeleteOutlined/>}
              title="Are you  delete this dataset?"
              key={record.id}
              onClick={() => deleteDataset(record)}
            >
              Delete
            </PopconfirmButton>
          </div>
        );
      }

    } 
  ]

  return (
    <div>
      <div style={{float: "right", paddingBottom: "5px"}}>
        <Button onClick={createDataset} type="primary">Create Dataset</Button>
      </div>
      <Table
        rowKey={"id"}
        scroll={{ x: "100%" }}
        columns={columns}
        dataSource={data}
        size={"small"}
      />
    </div>
  )

}
