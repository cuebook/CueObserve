import React, { useState, useEffect, useRef } from "react";
import style from "./style.module.scss";
import { useParams, useHistory } from 'react-router-dom';
import { Checkbox, Table, Icon } from "antd";
import { CaretUpOutlined, CaretDownOutlined } from '@ant-design/icons';

import AnomalyChart from "components/Anomalys/AnomalyChart";
import rootCauseAnalysisService from "services/rootCauseAnalysis";


export default function Anomaly(props) {
  const [ rcaData, setRCAData ] = useState(null);

  useEffect(() => {
    getRCA();
  }, []);


  const getRCA = async () => {
    const data = await rootCauseAnalysisService.getRCA(props.anomalyId)
    if (data) {
      setRCAData(data);
    }
  }

  if (!rcaData){
    return <p>Not yet</p>
  }

  const groupDataOnDimension = data => {
    let dimensionData = {}
    let dimensionContribution = {}
    data.forEach(row => {
      if (!dimensionData[row.dimension]){
        dimensionData[row.dimension] = []
        dimensionContribution[row.dimension] = 0
      }
      dimensionData[row.dimension].push(row)
      dimensionContribution[row.dimension] += row['data']['contribution']
    })

    let groupedData = Object.keys(dimensionData).map((dimension)=>[{dimension: dimension, dimensionContribution: dimensionContribution[dimension], rcaData: dimensionData[dimension]}])

    return [].concat.apply([], groupedData);
  }

  const groupedData = groupDataOnDimension(rcaData.rcaAnomalies)

  const subTableColumns = [
    {
      title: "Anomalous Segment",
      dataIndex: "dimensionValue",
      key: "dimensionValue",
      width: "42.86%",
      render: (text, record) => {
        let highOrLowIcon = null;
        let dimensionValueName = text
        try {
          highOrLowIcon =
            record.data.anomalyOnDate.highOrLow == "high" ? (
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
      title: "Contribution",
      dataIndex: "value",
      key: "value",
      align: "right",
      width: "14.28%",
      render: (text, record) => (
        <div style={{ display: "grid" }}>
          <div>{record.data.value}</div>
          <div style={{ fontSize: "12px" }}>({record.data.contribution}%)</div>
        </div>
      )
    },
    {
      title: "30-day Contribution",
      dataIndex: "data",
      key: "data",
      align: "center",
      width: "42.86%",
      render: (text, record) => {
        return (
          <div style={{ paddingTop: "8px" }}>
                  <AnomalyChart
                    data={ {data: text} }
                    isMiniChart={true}
                    // params={text}
                    // isMiniChart={true}
                    // disablePadding={true}
                    // height={65}
                    // key={record.filterText}
                    // anomalySize={3.5}
                    // lineColor="#178DF9BB"
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
      render: (text, record) => <h6>{text}</h6>
    },
    {
      title: "Contribution of Anomalous Segments",
      dataIndex: "dimensionContribution",
      width: "12%",
      align: "right",
      key: "dimensionContribution",
      sorter: (a, b) => a.dimensionContribution - b.dimensionContribution,
      defaultSortOrder: "descend",
      render: (text, record) => {
        return text + "%"
        // let contribution = Math.round((text / rowTotal) * 10000) / 100;
        // return (
        //   <div style={{ display: "grid" }}>
        //     <span>{text}</span>
        //     <span style={{ fontSize: "12px" }}>({contribution}%)</span>
        //   </div>
        // );
      }
    },
    {
      title: "Segments",
      children: [
        {
          title: "Anomalous Segment",
          dataIndex: "rcaData",
          key: "rcaData",
          align: "center",
          width: "30%",
          render: (text, record) => {
            let table = (
              <div className="rcaTableSub">
                <Table
                  columns={subTableColumns}
                  dataSource={text}
                  pagination={false}
                  scroll={{ y: "max-content" }}
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
                colSpan: 4
              }
            };
          }
        },
        {
          title: "Contribution",
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
          title: "30-day Contribution",
          dataIndex: "rcaData",
          key: "rcaData",
          align: "center",
          width: "30%",
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


  return (<>
    <h1>Root Cause Analysis</h1>
            <Table
              columns={tableColumns}
              dataSource={groupedData}
              pagination={false}
              scroll={{ y: "1000px" }}
              key="rcaTable"
              // bordered={true}
            />
  </>)

}
