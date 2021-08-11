import React, { useState, useEffect, useRef } from "react";
import style from "./style.module.scss";
import { useParams, useHistory } from 'react-router-dom';
import { Table, Button, Spin } from "antd";
import { CaretUpOutlined, CaretDownOutlined } from '@ant-design/icons';

import AnomalyChart from "components/Anomalys/AnomalyChart";
import rootCauseAnalysisService from "services/rootCauseAnalysis";
import RCALogs from "./rcaLogs"

export default function Anomaly(props) {
  const [ rcaData, setRCAData ] = useState(null);
  const [ loading, setLoading ] = useState(false);
  let refreshWorkflowRunsInterval

  useEffect(() => {
    if (!rcaData){
      getRCA();
    }

    return () => {
      clearInterval(refreshWorkflowRunsInterval);
    };

  }, []);


  const getRCA = async () => {
    const data = await rootCauseAnalysisService.getRCA(props.anomalyId)
    if (data) {
      setRCAData(data);
      if (!refreshWorkflowRunsInterval && ["RECEIVED", "RUNNING"].includes(data.status)){
        refreshWorkflowRunsInterval = setInterval(() => {
             getRCA()
           }, 3000);
      }

      if (["SUCCESS", "ERROR"].includes(data.status)){
        clearInterval(refreshWorkflowRunsInterval);
      }

    }
  }

  const doRCA = async () => {
    setLoading(true)
    const data = await rootCauseAnalysisService.doRCA(props.anomalyId)
    if (data){
      setLoading(false)
      getRCA()
    }
  }

  if (!rcaData){
    return <div className={` ${style.loadingDiv}`}>
          {" "}
          <Spin />{" "}
        </div>
  }

  const groupDataOnDimension = data => {
    let dimensionData = {}
    let dimensionMetricSummed = {}
    data.forEach(row => {
      if (!dimensionData[row.dimension]){
        dimensionData[row.dimension] = []
        dimensionMetricSummed[row.dimension] = 0
      }
      dimensionData[row.dimension].push(row)
      dimensionMetricSummed[row.dimension] += row['data']['anomalyLatest']['value']
    })

    let groupedData = Object.keys(dimensionData).map((dimension)=>[{dimension: dimension, dimensionMetricSummed: dimensionMetricSummed[dimension], rcaData: dimensionData[dimension]}])

    return [].concat.apply([], groupedData);
  }

  const groupedData = groupDataOnDimension(rcaData.rcaAnomalies)

  const subTableColumns = [
    {
      title: "Segment",
      dataIndex: "dimensionValue",
      key: "dimensionValue",
      width: "28.57%",
      render: (text, record) => {
        let highOrLowIcon = null;
        let dimensionValueName = text
        try {
          highOrLowIcon =
            record.data.anomalyLatest.highOrLow == "high" ? (
              <CaretUpOutlined style={{ color: "green" }} />
            ) : (
              <CaretDownOutlined style={{ color: "red" }} />
            );
        } catch (err) {}
        return (
          <div>
            {highOrLowIcon}
            <span className={style.segmentLabel}>{dimensionValueName}</span>
          </div>
        );
      }
    },
    {
      title: "Value",
      dataIndex: "value",
      key: "value",
      align: "right",
      width: "14.29%",
      render: (text, record) => {
        const percentage = record.data.anomalyLatest.value*100/rcaData.value
        const roundedPercentage = (Math.round(percentage * 100) / 100).toFixed(2);

        return (
          <div style={{ display: "grid" }}>
            <div>{record.data.anomalyLatest.value}</div>
            <div className="text-xs">({roundedPercentage}%)</div>
          </div>
        )
      }
    },
    {
      title: "",
      dataIndex: "data",
      key: "data",
      align: "center",
      width: "57.14%",
      render: (text, record) => {
        return (
                <div className="">
                  <AnomalyChart
                    data={ {data: text, metric: rcaData.measure, granularity: rcaData.granularity} }
                    isMiniChart={true}
                  />
                </div>
        );
      }
    }
  ];


  const tableColumns = [
    {
      title: "Dimension",
      dataIndex: "dimension",
      key: "dimension",
      width: "18%",
      render: (text, record) => <strong>{text}</strong>
    },
    {
      title: "Contribution of Anomalous Segments",
      dataIndex: "dimensionMetricSummed",
      width: "12%",
      align: "right",
      key: "dimensionMetricSummed",
      sorter: (a, b) => a.dimensionMetricSummed - b.dimensionMetricSummed,
      defaultSortOrder: "descend",
      render: (text, record) => {
        const percentage = text*100/rcaData.value
        return (Math.round(percentage * 100) / 100).toFixed(2) + "%";
      }
    },
    {
      title: "Anomalous Segments",
      children: [
        {
          title: "Segment",
          dataIndex: "rcaData",
          key: "rcaData",
          align: "center",
          width: "20%",
          render: (text, record) => {
            let table = (
              <div className="rcaTableSub">
                <Table
                  columns={subTableColumns}
                  dataSource={text}
                  pagination={false}
                  // scroll={{ y: "max-content" }}
                  // size="small"
                  showHeader={false}
                  key="rcaTableSub"
                  // bordered={true}
                />
              </div>
            );

            return {
              children: <a>{table}</a>,
              props: {
                colSpan: 3
              }
            };
          }
        },
        {
          title: "Value",
          dataIndex: "val",
          key: "val",
          align: "right",
          width: "10%",
          render: (text, record) => {
            return {
              children: null,
              props: {
                colSpan: 0
              }
            };
          }
        },
        {
          title: "",
          dataIndex: "rcaData",
          key: "rcaData",
          align: "center",
          width: "40%",
          render: (text, record) => {
            return {
              children: null,
              props: {
                colSpan: 0
              }
            };
          }
        }
      ]
    }
  ];


  const enabledAnalyzeButton = !loading && [null, 'SUCCESS', 'ERROR'].includes(rcaData.status)
  let anomalyTime = rcaData.anomalyTime.slice(0,10)
  anomalyTime += rcaData.granularity == "hour" ? " " + rcaData.anomalyTime.slice(11,16) : ""
  const filterPart = rcaData.dimension ? <>where <span style={{background:"#eeeeee", padding: "0 4px", borderRadius: "4px"}}>{rcaData.dimension} = {rcaData.dimensionValue}</span></> : null;

  return (<div className="">
            <div className={style.anomalyTitle}><strong>Root Cause Analysis</strong></div>
            <div className={`${style.anomalyText} mb-2`}>
              Analysis of <b>{rcaData.measure}</b> {filterPart} on {anomalyTime}
              <div>
                {rcaData.measure} = {rcaData.value}
              </div>
            </div>

            { <Button onClick={doRCA} disabled={!enabledAnalyzeButton} >Analyze</Button> }
            { rcaData.status && rcaData.status != "RECEIVED" ? <>
              <div className="my-2">
                <RCALogs data={rcaData} />
              </div> 
              <div className="rcaTable">
                <Table
                  columns={tableColumns}
                  dataSource={groupedData}
                  pagination={false}
                  // scroll={{ y: "1000px" }}
                  key="rcaTable"
                  width="100%"
                  // bordered={true}
                />
              </div>
            </> : null }
  </div>)

}
