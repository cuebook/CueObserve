import React, { useState, useEffect } from "react";
import style from "./style.module.scss";
import { Select } from "antd";

const { Option } = Select;

export default function PercentageChange(props){
  const [params, setParams] = useState({highOrLow: "high"});

    props.submitParams(params)

    return (
      <div className={style.paramBox}>
        Lifetime High/Low: <Select defaultValue="high" onChange={val => setParams({highOrLow: val})}>
            <Option value="high">High</Option>
            <Option value="low">Low</Option>
            </Select>
      </div>
    );
  }
