import React, { useState, useEffect, useRef } from "react";
import { Switch, Table, Button, Input, Drawer } from 'antd';
import {EditOutlined } from '@ant-design/icons';

import AddGlobalDimension from "components/Search/GlobalDimension/AddGlobalDimension.js"
import EditGlobalDimension from "components/Search/GlobalDimension/EditGlobalDimension.js"
import globalDimensionService from "services/search/globalDimension.js"
import style from "./style.module.scss"

const { Search } = Input
const ButtonGroup = Button.Group;

export default function GlobalDimensionTable(props) {
  const [globalDimension, setGlobalDimension] = useState('')
  const [data, setData] = useState('')
  const [isAddDrawerVisible, setIsAddDrawerVisible] = useState(false)
  const [isEditDrawerVisible, setIsEditDrawerVisible] = useState(false)
  const [editDimension, setEditDimension] = useState()
  useEffect(()=>{
    if(!data){
      getData()
    }
    
  }, []);


  const getData = async () => {
    const response = await globalDimensionService.getGlobalDimensions()
    setData(response)

  }

  const pubGlobalDimension = async (payload) => {
    const response = await globalDimensionService.publishGlobalDimension(payload)
    if(response.success){
      getData()
    }
  }

 const togglePublishState = (status, id) => {
    if (!id) {
      return;
    }

    let payload = {}
    payload["published"] = !status
    payload["id"] = id
    pubGlobalDimension(payload)
    
  };
  const closeAddDrawer = () =>  {
    setIsAddDrawerVisible(false)
    setIsEditDrawerVisible(false)
  }
  const openAddGlobalDimension = () => {
    setIsAddDrawerVisible(true)
  }
  const onAddGlobalDimensionSuccess = () =>{
    getData()

    setIsAddDrawerVisible(false)
  }
  const onEditGlobalDimensionSuccess = () =>{
    getData()
    setIsEditDrawerVisible(false)
  }

  const onClickEdit = ( val ) => {
    setIsEditDrawerVisible(true)
    setEditDimension(val)
  }



let dataSource = []
  dataSource = data && data.map(items=>{return {"name":items["name"], "id":items["id"],"published":items["published"] ,"values":items["values"].map((item)=> item["dataset"] + "."+ item["dimension"])}})
let linkedDimension = []
let linkedDimensionArray =[]
if(dataSource.length != 0){
  linkedDimension = dataSource.map((items) => items["values"])
  linkedDimensionArray = [].concat.apply([],linkedDimension)
}
    const columns = [
      {
        title: "Publish",
        dataIndex: "published",
        width: "10%",
        key: arr => arr.id,
        sorter: (a, b) => b.published - a.published,
        render: (text, entity) => {
          return (
            <Switch
              checked={entity.published}
              onChange={() =>
                togglePublishState(
                  entity.published,
                  entity.id
                )
              }
            />
          );
        }
      },
        {
          title: "Global Dimension",
          dataIndex: "name",
          key: "name",
          sorter: (a, b) => a.name.localeCompare(b.name),
          render: (text, entity) => {
            return (
              <span
                style={{ whiteSpace: "initial" }}
                key={entity.name}
              >
                {entity.name}
              </span>
            );
          }
        },
        {
          title: "Linked Dimensions",
          dataIndex: "values",
          key: "linkedDimension",
          render: (text, entity) => {
            let groupElements = entity.values
  
            var listIndividuals = groupElements.map(e => {
              return (
                <span
                  style={{
                    whiteSpace: "initial",
                    marginRight: "5px",
                    background: "#f4f5f6",
                    borderRadius: "4px",
                    padding: "1px 5px"
                  }}
                  key={e}
                >
                  {e}
                </span>
              );
            });
            return <div>{listIndividuals}</div>;
          }
        },
        {
          title: "",
          dataIndex: "action",
          key: "actions",
          className: "text-right",
          render: (text, record) => (
            <span className={style.actionButton}>
              <ButtonGroup className="mr-2">
                <Button
                  icon={<EditOutlined />}
                  onClick={e => onClickEdit(record)}
                />
              </ButtonGroup>
            </span>
          )
    
        } 
      ]


return (
  <div>

    <div className={`d-flex flex-column justify-content-center text-right mb-2`}>

      <Search
        style={{ margin: "0 0 10px 0" , width:350, float: "left"}}
        placeholder="Search"
        enterButton="Search"
        // onSearch={searchInDatasets}
        className="mr-2"
        />

      <Button onClick={openAddGlobalDimension} type="primary" >Add Global Dimension</Button>
</div>
    <Table
        rowKey={"id"}
        scroll={{ x: "100%" }}
        columns={columns}
        dataSource={dataSource}
        size={"small"}
        pagination={false}
      />
    <Drawer
          title={"Add Global Dimension"}
          width={720}
          onClose={closeAddDrawer}
          visible={isAddDrawerVisible}
        >
          { isAddDrawerVisible
            ? 
            <AddGlobalDimension onAddGlobalDimensionSuccess={onAddGlobalDimensionSuccess} linkedDimension={linkedDimensionArray} />
            :
            null
          }
    </Drawer> 

    <Drawer
          title={"Edit Global Dimension"}
          width={720}
          onClose={closeAddDrawer}
          visible={isEditDrawerVisible}
        >
          { isEditDrawerVisible 
            ? 
            <EditGlobalDimension editDimension={editDimension} linkedDimension={linkedDimensionArray} onEditGlobalDimensionSuccess={onEditGlobalDimensionSuccess}/>
            :
            null
          }
    </Drawer> 
  </div>
)

}

