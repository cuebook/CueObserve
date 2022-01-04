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
  Input,
  Switch
} from "antd";
import { EyeOutlined } from '@ant-design/icons';
import PopconfirmButton from "components/Utils/PopconfirmButton";
const {Search} = Input

const granularity = {
  "day" : "Day",
  "hour" : "Hour",
  "week" : "Week"
 }

 let today = new Date()

 function humanizeIsoTimestamp(timestamp, granularity){
  let hours = Math.floor((today.getTime() - Date.parse(timestamp))/(3600 * 1000))
  if(granularity === "hour")
  {
    return hours + " hours ago"
  }
  if(granularity === "day")
  {
    let days = Math.floor(hours/24)
    if(days <= 1)
    {
      return "Yesterday"
    }
    return days + " days ago"
  }
 }

export default function AnomalysTable(props) {
  const [currentPage, setCurrentPage] = useState(1);
  const [total, setTotal] = useState(0)
  const [limit] = useState(50);
  const [publishedOnly, setPublishedOnly]= useState(false);
  const [anomalys, setAnomalys] = useState(null);
  const [sorter, setSorter] = useState({})
  const [searchText, setSearchText] = useState("");
  const [searchedAnomaly, setSearchedAnomaly] = useState([]);
  const currentPageRef = useRef(currentPage);
  currentPageRef.current = currentPage;
  const currentPublishedOnlyRef = useRef(publishedOnly);
  currentPublishedOnlyRef.current = publishedOnly;
  const sorterRef = useRef(sorter);
  sorterRef.current = sorter;
  const searchTextRef = useRef(searchText);
  searchTextRef.current = searchText;
  const history = useHistory();

  useEffect(()=>{
    if (!anomalys){
      getAnomalys();
    }
  }, []);

  const getAnomalys = async (publishedOnly=currentPublishedOnlyRef.current, currentPage = currentPageRef.current, searchText = searchTextRef.current, sorter=sorterRef.current) => {
    const data = await anomalyService.getAnomalys(publishedOnly, (currentPage-1)*limit, limit, searchText, sorter)
    if (data && data.anomalies){
      setAnomalys(data.anomalies);
      setTotal(data.count)
    }
  }
  const viewAnomaly = async (anomaly) => {
    history.push('/anomaly/' + anomaly.id)
  }

  const getOnlyPublishedAnomalys = (event) => {
    setPublishedOnly(event)
    getAnomalys(event, currentPage)
  }
  const handleTableChange = (event, filter, sorter) => {
    setCurrentPage(event.current)
    setSorter({"columnKey":sorter.columnKey, "order":sorter.order})
    getAnomalys(publishedOnly, event.current,searchText ,{"columnKey":sorter.columnKey, "order":sorter.order})

  }
  const searchInAnomaly = (val) =>{
    setSearchText(val)
    setCurrentPage(1)
    getAnomalys(publishedOnly, 1, val)
  }

  const columns = [
    {
      title: "Dataset",
      dataIndex: "datasetName",
      key: "datasetName",
      sorter: () => {},
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
      sorter: () => {},
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
      sorter: () => {},
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
      sorter: () => {},
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
      sorter: () => {},
      render: (text, record) => {
        if(!record.data.contribution)
        return ""
        return (
          <p style={{float: "right"}}>{record.data.contribution.toFixed(2)}%</p>
        );
      }
    },
    {
      title: "Last Anomaly",
      dataIndex: "anomaly",
      key: "anomaly",
      sorter: () => {},
      render: (text, record) => {
        if(!record.data.anomalyLatest)
        return ""
        let percentColor = record.data.anomalyLatest.highOrLow == "high" ? "green" : "red"
        let percentSign = record.data.anomalyLatest.highOrLow == "high" ? "+" : "-"
        let percentDiv = record.data.anomalyLatest.percent?(<div><span style={{float: "right", color: percentColor}}>{percentSign}{record.data.anomalyLatest.percent.toFixed(0)}%</span></div>) : null
        return (
          <div>
          <div><span style={{float: "right"}}>{record.data.anomalyLatest.value}</span></div>
          <br />
          {percentDiv}
          </div>
        );
      }
    },
    {
      title: "Anomaly Time",
      dataIndex: "anomalyTimeISO",
      key: "anomalyTimeISO",
      sorter: () =>{},
      render: (text, record) => {
        if(!record.data.anomalyLatest)
        return ""
        return (
          <div>
          <p>{humanizeIsoTimestamp(record.data.anomalyLatest.anomalyTimeISO, record.granularity)}</p>
          </div>
        );
      }
    }
  ]


  return (
    <div>
      <div className={`d-flex flex-column justify-content-center text-right mb-2`}>
          <Search
              style={{ margin: "0 0 10px 0" , width:350, float: "left"}}
              placeholder="Search"
              enterButton="Search"
              onSearch={e=>{searchInAnomaly(e)}}
              className="mr-2"
            />
          <div>
            Published Only: <Switch onChange={getOnlyPublishedAnomalys} />  
          </div> 
      </div>
      <Table
        onRow={(record) => ({
          onClick: () => viewAnomaly(record)
        })}
        rowClassName={style.row}
        rowKey={"id"}
        scroll={{ x: "100%" }}
        onChange={handleTableChange}
        columns={columns}
        dataSource={anomalys}
        pagination={{
          showSizeChanger: false,
          current: currentPage,
          pageSize : limit,
          total : anomalys ? total : 50
        }}
        size={"small"}
      />
    </div>
  )

}
