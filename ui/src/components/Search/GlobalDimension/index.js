import React, { useState, useEffect, useRef } from "react";
import { Switch, Table, Button, Input, Drawer } from 'antd';
import {EditOutlined } from '@ant-design/icons';

import AddGlobalDimension from "components/Search/GlobalDimension/AddGlobalDimension.js"
import globalDimensionService from "services/search/globalDimension.js"
import style from "./style.module.scss"

const { Search } = Input
const ButtonGroup = Button.Group;

export default function GlobalDimensionTable(props) {
  const [globalDimension, setGlobalDimension] = useState('')
  const [data, setData] = useState('')
  const [isAddDrawerVisible, setIsAddDrawerVisible] = useState('')
  useEffect(()=>{
    if(!data){
      getData()
    }
    
  }, []);


  const getData = async () => {
    const response = await globalDimensionService.getGlobalDimension()
    setData(response)
    console.log("response", response)

  }





 const togglePublishState = (status, id) => {
    if (!id) {
      return;
    }

    const { dispatch } = this.props;

    // if (status) {
    //   dispatch({
    //     type: globalDimensionsActions.UNPUBLISH_GLOBAL_DIMENSION,
    //     payload: id
    //   });
    // } else {
    //   dispatch({
    //     type: globalDimensionsActions.PUBLISH_GLOBAL_DIMENSION,
    //     payload: id
    //   });
    // }
  };
  const closeAddDrawer = () =>  {
    setIsAddDrawerVisible(false)
  }
  const openAddGlobalDimension = () => {
    setIsAddDrawerVisible(true)
  }
  const onAddGlobalDimensionSuccess = () =>{
    setIsAddDrawerVisible(false)
  }

let dataSource = []
dataSource = data && data.map(items=>{return {"name":items["name"], "id":items["id"], "values":items["values"].map((item)=> item["dimensionName"])}})


    const columns = [
      {
        title: "Publish",
        dataIndex: "published",
        width: "10%",
        key: arr => arr[0].globalDimension.id,
        render: (text, entity) => {
          return (
            <Switch
              checked={false}
              // onChange={() =>
              //   togglePublishState(
              //     entity[0].globalDimension.published,
              //     entity[0].globalDimension.id
              //   )
              // }
            />
          );
        }
      },
        {
          title: "Global Dimension",
          dataIndex: "name",
          key: "name",
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
                  // icon={<EditOutlined />}
                  onClick={e => this.onClickEdit(record.id)}
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

      <Button onClick={openAddGlobalDimension} type="primary">Add Global Dimension</Button>
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
            <AddGlobalDimension onAddGlobalDimensionSuccess={onAddGlobalDimensionSuccess} />
            :
            null
          }
    </Drawer> 
  </div>
)








}

