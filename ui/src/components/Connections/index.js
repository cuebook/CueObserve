import React, { useState, useEffect } from "react";
import { Table, Button, Popconfirm, Input, message, Tooltip, Drawer, Modal} from "antd";
import style from "./style.module.scss";
import connectionService from "services/connection.js";
import AddConnection from "./AddConnection.js";
import ViewConnection from "./ViewConnection.js";
import { EyeOutlined, DeleteOutlined } from '@ant-design/icons';
const { Search } = Input;
const ButtonGroup = Button.Group;

export default function Connection() {
  const [connections, setConnections] = useState([]);
  const [selectedConnection, setSelectedConnection] = useState('');
  const [isAddConnectionDrawerVisible, setIsAddConnectionDrawerVisible] = useState('');
  const [isViewConnectionDrawerVisible, setIsViewConnectionDrawerVisible] = useState('');

  useEffect(() => {
    if (!connections.length) {
        fetchConnections();
    }
  }, []);

  const fetchConnections = async () => {
    const response = await connectionService.getConnections();
    setConnections(response.data)
  }

  const deleteConnection = async (connection) => {
    if (connection.datasetCount > 0){
      message.error("Connection linked with datasets can't be deleted");
      return ;
    }
    const response = await connectionService.deleteConnection(connection.id);
    if(response.success){
        fetchConnections()
    }
    else{
        message.error(response.message)
    }
  }

  const viewConnection = async (connection) => {
    setSelectedConnection(connection)
    setIsViewConnectionDrawerVisible(true)
  }

  const closeViewConnectionDrawer = () => {
    setIsViewConnectionDrawerVisible(false)
  }

  const closeAddConnectionDrawer = () => {
    setIsAddConnectionDrawerVisible(false)
  }

  const openAddConnectionForm = () => {
    setIsAddConnectionDrawerVisible(true)
  }

  const onAddConnectionSuccess = async () => {
    closeAddConnectionDrawer();
    fetchConnections();
  }


    const columns = [
      {
        title: "Connection Name",
        dataIndex: "name",
        key: "name",
        sorter: (a, b) => a.name.localeCompare(b.name)

      },
      {
        title: "Connection Type",
        dataIndex: "connectionType",
        key: "connectionType",
        sorter: (a, b) => a.connectionType.localeCompare(b.connectionType),
        render: (connectionType) => (
            <>
            <div className={style.connectionLogoTable} style={{backgroundImage: `url(${require("assets/img/" + connectionType + ".svg")})`}}>
            </div>
            {connectionType}
            </>
        )

      },
      {
        title: "Datasets",
        dataIndex: "datasetCount",
        key: "dataset",
        width: "10%",
        align: "right",
        sorter:(a, b) => a.datasetCount - b.datasetCount,
      },
      {
        title: "",
        dataIndex: "",
        key: "",
        width: "20%",
        render: (text, connection) => (
         <div className={style.actions}>
            <Tooltip title={"View Connection"}>
              <EyeOutlined onClick={() => viewConnection(connection)} />
            </Tooltip>
            <Popconfirm
                title={"Are you sure to delete "+ connection.name +"?"}
                onConfirm={() => deleteConnection(connection)}
                // onCancel={cancel}
                okText="Yes"
                cancelText="No"
            >
                <Tooltip title={"Delete Connection"}>
                    <DeleteOutlined />
                </Tooltip>
            </Popconfirm>
          </div>
        )
      }
    ];

    return (
      <div>
        <div className={`d-flex flex-column justify-content-center text-right mb-2`}>
            <Button
                key="createTag"
                type="primary"
                onClick={() => openAddConnectionForm()}
            >
                Add Connection
            </Button>
        </div>
        <Table
            rowKey={"id"}
            scroll={{ x: "100%" }}
            columns={columns}
            dataSource={connections}
            size={"small"}
            pagination={{
              defaultPageSize:50,
              total:  connections ? connections.length : 50
            }}
        />

        <Drawer
          title={"Add Connection"}
          width={720}
          onClose={closeAddConnectionDrawer}
          visible={isAddConnectionDrawerVisible}
        >

          { isAddConnectionDrawerVisible 
                ? 
                <AddConnection  onAddConnectionSuccess={onAddConnectionSuccess}/>
                :
                null
              }
        </Drawer>
        <Drawer
          title={selectedConnection.name}
          width={720}
          onClose={closeViewConnectionDrawer}
          visible={isViewConnectionDrawerVisible}
        >
          { isViewConnectionDrawerVisible 
            ? 
            <ViewConnection connection={selectedConnection} />
            :
            null
          }
        </Drawer>

    </div>
    );
  }