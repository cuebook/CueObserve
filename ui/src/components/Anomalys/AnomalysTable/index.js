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
import { EyeOutlined } from '@ant-design/icons';
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

  const viewAnomaly = async (anomaly) => {
    history.push('/anomaly/' + anomaly.id)
  }

  const columns = [
    {
      title: "Title",
      dataIndex: "title",
      key: "title",
      sorter: (a, b) => a.title.localeCompare(b.title),
      render: text => {
        return (
          <p>{text}</p>
        );
      }
    },
    {
      title: "Filter",
      dataIndex: "dimVal",
      key: "dimVal",
      sorter: (a, b) => a.dimVal.localeCompare(b.dimVal),
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
      render: (text, record) => {
        return (
          <div className={style.actions}>
             <Tooltip title={"View Anomaly"}>
                 <EyeOutlined onClick={()=>viewAnomaly(record)} />
             </Tooltip>
           </div>
        );
      }
    },
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
