import React, { useState, useEffect } from "react";
import style from "./style.module.scss";
import { InputNumber } from "antd";

export default function PercentageChange(props){
  const [params, setParams] = useState({});

    props.submitParams(params)

    return (
      <div className={style.paramBox}>
        Percentage Threshold: <InputNumber min={1} onChange={val => setParams({threshold: val})} /> 
      </div>
    );
  }
