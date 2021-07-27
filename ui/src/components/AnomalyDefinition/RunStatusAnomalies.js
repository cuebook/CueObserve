import React, { useState, useEffect, useRef } from "react";
import style from "./style.module.scss";

import { Table } from "antd";

import anomalyDefService from "services/anomalyDefinitions.js";

export default function RunStatusAnomalies(props) {
  
  const [runStatusAnomalies, setRunStatusAnomalies] = useState('');
  const [loading, setLoading] = useState('');
  
  useEffect(() => {
    console.log(props)
    getRunStatusAnomalies(props.runStatusId);
  }, [props]);

  const getRunStatusAnomalies = async (runStatusId) => {
    setLoading(true)
    const response = await anomalyDefService.getRunStatusAnomalies(runStatusId);
    setRunStatusAnomalies(response);
    setLoading(false)
  };


  const columns = [
    {
      title: "Dimension Value",
      dataIndex: "dimensionVal",
      key: "dimensionVal",
      width: "25%",
      render: (text, record) => {
        return (
          <span>
            <a href={"#/anomaly/"+record.id} className={style.linkText}>{text}</a>
          </span>
        );
      }
    },
    {
        title: "Published",
        dataIndex: "published",
        key: "published",
        width: "15%",
        render: text => {
          return (
            <span>
              {text ? "True" : "False"}
            </span>
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
        dataSource={runStatusAnomalies}
        loading={loading}
        size={"small"}
      />
    </div>
  );
}
