import React, { useState } from "react";
import { Popconfirm, Button } from "antd";

export default function PopconfirmButton(props) {
  const [visible, setVisible] = React.useState(false);

  const handleOk = () => {
    setVisible(false);
    props.onClick();
  };

  return (
    <>
      <Popconfirm
        title={props.title}
        visible={visible}
        onConfirm={handleOk}
        okText="Yes"
        cancelText="No"
        // okButtonProps={{  }}
        onCancel={() => setVisible(false)}
      >
        <Button
          icon={props.icon ? props.icon : null}
          onClick={() => setVisible(true)}
        >
          {props.children}
        </Button>
      </Popconfirm>
    </>
  );
}