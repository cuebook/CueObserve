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

const granularity = {
  "day" : "Day",
  "hour" : "Hour",
  "week" : "Week"
 }

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
      title: "Dataset",
      dataIndex: "datasetName",
      key: "datasetName",
      sorter: (a, b) => a.datasetName.localeCompare(b.datasetName),
      render: text => {
        return (
          <p>{text}</p>
        );
      }
    },
    {
      title: "Granularity",
      dataIndex: "granularity",
      key: "granularity",
      sorter: (a, b) => a.granularity.localeCompare(b.granularity),
      render: text => {
        return (
          <p>
            {granularity[text]}
          </p>
        )
      }
    },
    {
      title: "Measure",
      dataIndex: "metric",
      key: "metric",
      sorter: (a, b) => a.metric.localeCompare(b.metric),
      render: text => {
        return (
          <p>{text}</p>
        );
      }
    },
    {
      title: "Filter",
      dataIndex: "dimensionVal",
      key: "dimensionVal",
      sorter: (a, b) => a.dimensionVal.localeCompare(b.dimensionVal),
      render: (text, record) => {
        return (
          <p>{record.dimension} = {text}</p>
        );
      }
    },
    {
      title: "Filter's Contribution",
      dataIndex: "contribution",
      key: "contribution",
      sorter: (a, b) => a.data.contribution > b.data.contribution ? 1 : -1,
      render: (text, record) => {
        return (
          <p>{record.data.contribution} %</p>
        );
      }
    },
    {
      title: "Latest Anomaly",
      dataIndex: "anomalyTimeStr",
      key: "anomalyTimeStr",
      sorter: (a, b) => a.anomalyTimeStr.localeCompare(b.anomalyTimeStr),
      render: (text, record) => {
        return (
          <p>
          <div>{text}</div>
          <div>Actual Value: {record.data.anomalyLatest.value}</div>
          <div>% Deviation: {record.data.anomalyLatest.percent}</div>
          </p>
        );
      }
    }
  ]

  return (
    <div>
      <Table
        onRow={(record) => ({
          onClick: () => viewAnomaly(record),
        })}
        rowKey={"id"}
        scroll={{ x: "100%" }}
        columns={columns}
        dataSource={anomalys}
        size={"small"}
      />
    </div>
  )

}
