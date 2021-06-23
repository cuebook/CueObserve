import React, { useState, useEffect, useRef } from "react";
import TimeAgo from 'react-timeago';
import _ from "lodash";
import anomalyService from "services/anomalys.js";
import style from "./style.module.scss";
import { useHistory } from "react-router-dom";
import {
  Table,
} from "antd";
import { MoreOutlined, PlayCircleOutlined, UnorderedListOutlined, StopOutlined, FileTextOutlined, DeleteOutlined, CopyOutlined, CloseOutlined, EditOutlined } from '@ant-design/icons';

export default function AnomalyTable() {
  const [data, setData] = useState([]);

  useEffect(()=>{
    if (!data.length){
      getData();
    }
  }, []);

  const getData = async () => {
    const data = await anomalyService.getAnomalys()
    console.log(data)
    if (data && data.length){
      setData(data);
    } 
  }

  const columns = [
    {
      title: "Anomalys",
      dataIndex: "name",
      key: "name",
      width: "20%",
      sorter: ()=>{},
      ellipsis: true,

      render: text => {
        return (
          <p>{text}</p>
        );
      }
    }
  ]

  return <Table
    rowKey={"id"}
    scroll={{ x: "100%" }}
    columns={columns}
    dataSource={data}
    size={"small"}
  />

}
