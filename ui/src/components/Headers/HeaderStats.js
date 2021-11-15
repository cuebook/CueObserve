import React from "react";
import { Affix } from "antd";
import TopBar from "components/layout/TopBar"
import style from "./style.module.scss"

export default function HeaderStats() {
  return (
    <>
      {/* Header */}
      <Affix>
      <div style={{zIndex:9999}}>
        <TopBar />
      </div>
      </Affix>
    </>
  );
}