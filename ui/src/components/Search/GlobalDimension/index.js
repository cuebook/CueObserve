import React, { useState, useEffect, useRef } from "react";
import { Switch, Table, Button, Input, Drawer } from 'antd';

import AddGlobalDimension from "components/Search/GlobalDimension/AddGlobalDimension.js"

const { Search } = Input

export default function GlobalDimensionTable(props) {
  const [globalDimension, setGlobalDimension] = useState([])
  const [isAddDrawerVisible, setIsAddDrawerVisible] = useState('')
  useEffect(()=>{
    
    
  }, []);




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

    const columns = [
      {
        title: "Publish",
        dataIndex: "published",
        width: "10%",
        key: arr => arr[0].globalDimension.id,
        render: (text, entity) => {
          return (
            <Switch
              checked={entity[0].globalDimension.published}
              onChange={() =>
                togglePublishState(
                  entity[0].globalDimension.published,
                  entity[0].globalDimension.id
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
        },
        {
          title: "Linked Dimensions",
          dataIndex: "linkedDimension",
          key: "linkedDimension",
        },
        {
          title: "",
          dataIndex: "action",
          key: "actions",
          className: "text-right",
          
    
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
        dataSource={[]}
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

