import React, { useState, useEffect, useRef } from "react";
import TimeAgo from 'react-timeago';
import _ from "lodash";
import anomalyService from "services/anomalys";
import style from "./style.module.scss";
import { useHistory } from "react-router-dom";
import {search} from "services/general.js"
import {
  Table,
  Button,
  Popconfirm,
  Tooltip,
  Input
} from "antd";
import { EyeOutlined } from '@ant-design/icons';
import PopconfirmButton from "components/Utils/PopconfirmButton";
const {Search} = Input

const granularity = {
  "day" : "Day",
  "hour" : "Hour",
  "week" : "Week"
 }

export default function AnomalysTable(props) {
  const [anomalys, setAnomalys] = useState(null);
  const [searchText, setSearchText] = useState("");
  const [searchedAnomaly, setSearchedAnomaly] = useState([]);

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
      sorter: (a, b) => {
        a= a.dimensionVal || "";
        b= b.dimensionVal ||  "";
        return a.localeCompare(b)},
      render: (text, record) => {
        return text ? (
          <p>{record.dimension} = {text}</p>
        ) : "";
      }
    },
    {
      title: "Filter's Contribution",
      dataIndex: "contribution",
      key: "contribution",
      sorter: (a, b) => a.data.contribution > b.data.contribution ? 1 : -1,
      render: (text, record) => {
        return (
          <p style={{float: "right"}}>{record.data.contribution.toFixed(2)}%</p>
        );
      }
    },
    {
      title: "Last Anomaly",
      dataIndex: "anomaly",
      key: "anomaly",
      sorter: (a, b) => a.data.anomalyLatest.percent > b.data.anomalyLatest.percent ? 1 : -1,
      render: (text, record) => {
        let percentColor = record.data.anomalyLatest.highOrLow == "high" ? "green" : "red"
        let percentSign = record.data.anomalyLatest.highOrLow == "high" ? "+" : "-"
        return (
          <div>
          <div><span style={{float: "right"}}>{record.data.anomalyLatest.value}</span></div>
          <br />
          <div><span style={{float: "right", color: percentColor}}>{percentSign}{record.data.anomalyLatest.percent}%</span></div>
          </div>
        );
      }
    },
    {
      title: "Anomaly Time",
      dataIndex: "anomalyTimeStr",
      key: "anomalyTimeStr",
      sorter: (a, b) => a.anomalyTimeStr.localeCompare(b.anomalyTimeStr),
      render: (text, record) => {
        return (
          <div>
          <p>{text}</p>
          </div>
        );
      }
    }
  ]
const searchInAnomaly = (val) =>{
  setSearchText(val)
  let convertedAnomaly = search(anomalys, ["datasetName", "granularity", "metric", "dimensionVal"], val)
  setSearchedAnomaly(convertedAnomaly)
}


  return (
    <div>
      <div className={`d-flex flex-column justify-content-center text-right mb-2`}>
        <div style={{marginTop: -8}}>
          <Search
              style={{ margin: "0 0 10px 0" , width:350, float: "left"}}
              placeholder="Search"
              enterButton="Search"
              onSearch={e=>{searchInAnomaly(e)}}
              className="mr-2"
            />
          </div>
      </div>
      <Table
        onRow={(record) => ({
          onClick: () => viewAnomaly(record),
        })}
        rowKey={"id"}
        scroll={{ x: "100%" }}
        columns={columns}
        dataSource={ searchText.length > 0 ? searchedAnomaly: anomalys}
        pagination={{
          pageSize : 50,
          total : columns ? columns.length : 50
        }}
      />
    </div>
  )

}
