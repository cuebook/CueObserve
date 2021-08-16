import React, { useState, useEffect } from "react";
import style from "./style.module.scss";
import { Select, InputNumber } from "antd";

const { Option } = Select;

export default function ValueThreshold(props){
    const [operator, setOperator] = useState("greater");
    const [params, setParams] = useState({});

    let inputElement = null

    const onChangeOperator = operator => {
      setOperator(operator)
      setParams({})
    }

    if(operator == "greater")
    {
      inputElement = (<div className={style.paramBox}>
        Lower Threshold: <InputNumber min={1} onChange={val => setParams({lowerThreshold: val, upperThreshold: "null"})} /> 
      </div>)
    }
    if(operator == "lesser")
    {
      inputElement = (<div className={style.paramBox}>
        Upper Threshold: <InputNumber min={1} onChange={val => setParams({lowerThreshold: "null", upperThreshold: val})} /> 
      </div>)
    }
    if(operator == "between")
    {
      inputElement = (
      <div>
        <div className={style.paramBox}>
        Lower Threshold: <InputNumber min={1} onChange={val => setParams(param => {return {...param, lowerThreshold: val}})} />
        </div>
        <div className={style.paramBox}>
        Upper Threshold: <InputNumber min={1} onChange={val => setParams(param => {return {...param, upperThreshold: val}})} />
      </div>
      </div>)
    }
  
    props.submitParams(params)


    return (
      <div>
      <div className={style.paramBox}>
        Operator: <Select defaultValue="greater" onChange={val => onChangeOperator(val)}>
            <Option value="greater">Greater than</Option>
            <Option value="lesser">Less than</Option>
            <Option value="between">In between</Option>
            </Select>
            </div>
            <div className={style.paramBox}>{inputElement}</div>
      </div>
    );
  }
