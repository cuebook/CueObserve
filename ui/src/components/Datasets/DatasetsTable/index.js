import React, { useState, useEffect, useRef } from "react";
import TimeAgo from 'react-timeago';
import _ from "lodash";
import datasetService from "services/datasets";
import style from "./style.module.scss";
import { useHistory } from "react-router-dom";
import {
  Table,
  Button,
  Popconfirm,
  Tooltip,
  Input
} from "antd";
import { DeleteOutlined, EditOutlined } from '@ant-design/icons';
import PopconfirmButton from "components/Utils/PopconfirmButton";
import { search } from "services/general.js";
 const {Search} = Input

export default function DatasetsTable(props) {
  const [datasets, setDatasets] = useState(null);
  const history = useHistory();
  const [searchText, setSearchText] = useState("");
  const [searchedDatasets, setSearchedDatasets] = useState([]);

  useEffect(()=>{
    if (!datasets){
      getDatasets();
    }
  }, []);

  const getDatasets = async () => {
    const data = await datasetService.getDatasets()
    if (data && data.length){
      setDatasets(data);
    }
  }

  const deleteDataset = async (record) => {
    const response = await datasetService.deleteDataset(record.id)
    if (response){
      getDatasets()
    }
  }

  const editDataset = record => {
    history.push('/dataset/' + record.id)
  }

  const createDataset = () => {
    history.push("/dataset/create")
  }

  const searchInDatasets = (val) =>{
    setSearchText(val)
    let convertedDatasets = search(datasets, ["name", "connectionName", "granularity"], val)
    setSearchedDatasets(convertedDatasets)
  }
  const columns = [
    {
      title: "Dataset Name",
      dataIndex: "name",
      key: "name",
      sorter: (a, b) => a.name.localeCompare(b.name),
    },
    {
      title: "Connection",
      dataIndex: "connection",
      key: "connection",
      sorter: (a, b) => a.connection.name.localeCompare(b.connection.name),
      render: connection => { return connection.name}
    },
    {
      title: "Granularity",
      dataIndex: "granularity",
      key: "granularity",
      sorter: (a, b) => a.granularity.localeCompare(b.granularity),
      render: granularity => { return _.capitalize(granularity) }
    },
    {
      title: "Anomaly Definitions",
      dataIndex: "anomalyDefinitionCount",
      key: "anomalyDefinitionCount",
      className: "text-right",
      sorter: (a, b) => a.anomalyDefinitionCount - b.anomalyDefinitionCount,
    },
    {
      title: "",
      dataIndex: "action",
      key: "actions",
      className: "text-right",
      render: (text, record) => {
        return (
          <div className={style.actions}>
             <Tooltip title={"View Dataset"}>
                 <EditOutlined onClick={()=>editDataset(record)} />
             </Tooltip>
             { record.anomalyDefinitionCount ? null :
               <Popconfirm
                   title={"Are you sure to delete '"+ record.name +"'?"}
                   onConfirm={() => deleteDataset(record)}
                   // onCancel={cancel}
                   okText="Yes"
                   cancelText="No"
               >
                   <Tooltip title={"Delete Dataset"}>
                       <DeleteOutlined />
                   </Tooltip>
               </Popconfirm>
             }
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
          onSearch={searchInDatasets}
          className="mr-2"
          />
      
        <Button onClick={createDataset} type="primary">Add Dataset</Button>
      </div>
      <Table
        rowKey={"id"}
        scroll={{ x: "100%" }}
        columns={columns}
        dataSource={ searchText.length > 0 ? searchedDatasets : datasets}
        size={"small"}
        pagination={{
          defaultPageSize:50,
          total:  searchText.length > 0 ? searchedDatasets.length : datasets ? datasets.length : 50
        }}
      />
    </div>
  )

}
