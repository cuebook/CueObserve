import React, { useState, useEffect, useRef } from "react";
import style from "./style.module.scss";
import Moment from 'react-moment';

import { Table } from "antd";

import anomalyDefService from "services/main/anomalyDefinitions.js";
var moment = require("moment");

function timehumanize(temps){
  var obj = "";
  for (var temp of temps) {
    if(temp.slice(-1) == "s"){
      
      temp = temp.slice(0,-1)
    } 
    obj = obj+" "+temp
  }
  return obj;
}

export default function RunStatus(props) {

  const [detectionRuns, setDetectionRuns] = useState('');
  const [loading, setLoading] = useState('');
  const [currentPage, setCurrentPage] = useState('');
  
  useEffect(() => {
    if (!detectionRuns) {
        setCurrentPage(1)
        getDetectionRuns(props.anomalyDef.id, 0);
    }
  }, []);

  const parseLogs = (logs) => {
    let logElement = <div className={style.logsDiv}>{logs.log}</div>
    return logElement
  }

  const getDetectionRuns = async (anomalyDefId, offset) => {
    setLoading(true)
    const response = await anomalyDefService.getDetectionRuns(anomalyDefId, offset);
    setDetectionRuns(response);
    setLoading(false)
  };

  const handleTableChange = (event) => {
    setCurrentPage(event.current)
    getDetectionRuns(props.anomalyDef.id, (event.current - 1)*10)
  }


  const columns = [
    {
      title: "Run Status",
      dataIndex: "status",
      key: "status",
      width: "15%",
      render: text => {
        return (
          <span>
            {text}
          </span>
        );
      }
    },
    {
        title: "Run Type",
        dataIndex: "runType",
        key: "runType",
        width: "15%",
        render: text => {
          return (
            <span>
              {text}
            </span>
          );
        }
      },
    {
      title: "Run Timestamp",
      dataIndex: "startTimestamp",
      key: "startTimestamp",
      width: "30%",
      render: text => {
        return (
          <span>
            {text}
          </span>
        );
      }
    },
    {
      title: "Duration",
      dataIndex: "",
      key: "",
      width: "10%",
      // align:"center",
      render: (text ,record) => {
        let timeDiff;
        if (record && record.startTimestamp && record.endTimestamp){
          timeDiff = Math.round((new Date(record.endTimestamp) - new Date(record.startTimestamp))/1000)

        }
        let diff;
        if (timeDiff){
          diff =  moment.duration(timeDiff, "second").format("h [hrs] m [min] s [sec]", {
            trim: "both"
        });
        }
        if(diff){
          diff = timehumanize(diff.split(" "))
        }
        let item = (
          <div> 
            {diff}
          </div>
        )
        return (
          <span>
            {item} 
          </span>
        );
      }
    },
    {
      title: "Anomalies",
      dataIndex: "anomalies",
      key: "anomalies",
      width: "10%",
      // align:"center",
      render: (text ,record) => {
        return (
          <span>
            {record.logs.numAnomaliesPulished} {record.logs.numAnomalySubtasks?("("+record.logs.numAnomalySubtasks+")"):""} 
          </span>
        );
      }
    },
    {
      title: "",
      dataIndex: "logs",
      key: "logs",
      width: "10%",
      render: (text) => {
        return (
          <a>Logs</a>
        );
      }
  }
  ]

  return (
    <div className={style.runLogTable}>
      <Table
        rowKey={"id"}
        scroll={{ x: "100%" }}
        columns={columns}
        dataSource={detectionRuns.runStatuses}
        loading={loading}
        size={"small"}
        pagination={{
          current: currentPage,
          pageSize: 10,
          total: detectionRuns ? detectionRuns.count : 0
        }}
        expandable={{
          expandedRowRender: runStatus => parseLogs(runStatus.logs),
          expandRowByClick: true,
          expandIconColumnIndex: -1
        }}
        onChange={(event) => handleTableChange(event)}
      />
    </div>
  );
}
