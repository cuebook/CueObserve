import React, { useState, useEffect, useRef } from "react";
import TimeAgo from 'react-timeago';
import _ from "lodash";
import anomalyService from "services/anomalys";
import style from "./style.module.scss";
import { useHistory } from "react-router-dom";
import {
  Table,
  Button,
  Popconfirm,
  Tooltip
} from "antd";
import { MoreOutlined, PlayCircleOutlined, UnorderedListOutlined, StopOutlined, FileTextOutlined, DeleteOutlined, CopyOutlined, CloseOutlined, EditOutlined } from '@ant-design/icons';
import PopconfirmButton from "components/Utils/PopconfirmButton";

export default function AnomalysTable(props) {
  const [anomalys, setAnomalys] = useState(null);
  const history = useHistory();

  useEffect(()=>{
    if (!anomalys){
      getAnomalys();
    }
  }, []);

  const getAnomalys = async () => {
    const data = await anomalyService.getAnomalys()
    if (data && data.length){
      setAnomalys(data);
    }
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
    } 
  ]

  return (
    <div>
      <Table
        rowKey={"id"}
        scroll={{ x: "100%" }}
        columns={columns}
        dataSource={anomalys}
        size={"small"}
      />
    </div>
  )

}
