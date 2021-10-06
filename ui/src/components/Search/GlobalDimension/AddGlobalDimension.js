import React, { useState, useEffect, useRef } from "react";
import { Button, Form, Input, Switch, message, Select } from "antd";
import style from "./style.module.scss";

import searchService from "services/main/search.js"
import globalDimensionService from "services/search/globalDimension.js"

const { Option } = Select;

export default function AddGlobalDimension(props) {
    const [form] = Form.useForm();

    const [globalDimension, setGlobalDimension] = useState([])
    const [dimensions, setDimensions] = useState(null)
    const [selectedDimension, setSelectedDimension] = useState([])
    useEffect(()=>{
      if(!dimensions){
        getDimension()
      }
      
    }, []);

    const getDimension = async () => {
        const response = await globalDimensionService.getDimensions()
        console.log("response", response)
        setDimensions(response)
    }

    const onSelectChange = value => {
      setSelectedDimension(value)
      console.log("value", value)
    }

    const addGlobalDimensionFormSubmit = async (values) => {
        let payload = {
        };
        console.log("values on form submit", values)
        let dimensionalValues = []
        dimensionalValues = values["dimension"].map((value)=> {
          let temp = value.split(".");
          return {
            "datasetId":temp[0],
            "datasetName":temp[1],
            "dimension":temp[2],
        }})
        payload["name"] = values["name"]
        payload["dimensionalValues"] = dimensionalValues 
        // Create Global Dimension 
        // createGlobalDimension(payload)
        props.onAddGlobalDimensionSuccess()

        const response = await globalDimensionService.AddGlobalDimension(payload)

        // if(response.success){
        //     props.onAddGlobalDimensionSuccess()
        // }
        // else{
        //     message.error(response.message);
        // }
      };
    
  // const createGlobalDimension = async (payload) => {
  //   const response = await searchService.AddGlobalDimension(payload)
  // }

  const children = [];
    for (let i = 10; i < 36; i++) {
      children.push(<Option key={i.toString(36) + i}>{i.toString(36) + i}</Option>);
    }

    let dimensionForSuggestion = []
    dimensionForSuggestion = dimensions && dimensions.map(item =>(<Option key={item["datasetId"] + "." + item["datasetName"] + "." + item["dimension"]} > {item["datasetName"] + "." + item["dimension"]} </Option>))

    console.log("dimesionForSuggestion", dimensionForSuggestion)
    let addGlobalDimensionParamElements = []

    let addGlobalDimensionFormElement = (
      <div>
        <Form 
            layout="vertical" 
            className="mb-2" 
            form={form} 
            onFinish={addGlobalDimensionFormSubmit}
            name="addSchedule"
            scrollToFirstError
            hideRequiredMark
        >
          <div className={style.addConnectionForm}>
            <div className={style.formItem} style={{ width: "100%" }}>

            <Form.Item hasFeedback name="name" >
                <Input className={style.inputArea} placeholder={"Global Dimension Name"}/>
              </Form.Item>
            <Form.Item name ="dimension">
              <Select showSearch  mode="tags" style={{width: "100%"}} placeholder="Select Dimension" onChange={onSelectChange}>
                {dimensionForSuggestion}
              </Select>
            </Form.Item>
            </div>
            {addGlobalDimensionParamElements}
          </div>
          <div className={style.submitButton}>
            <Button
                icon=""
                type="primary"
                className="mr-2"
                htmlType="submit"
            >
                Add Global Dimension
            </Button>
          </div>
        </Form>
      </div>
    );


    return (
      <div>
        <div className="row">
            <div>
              {addGlobalDimensionFormElement}
            </div>
          
        </div>
      </div>
    );
}