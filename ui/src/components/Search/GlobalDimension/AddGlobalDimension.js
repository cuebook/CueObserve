import React, { useState, useEffect, useRef } from "react";
import { Button, Form, Input, Switch, message, Select } from "antd";
import style from "./style.module.scss";

import globalDimensionService from "services/search/globalDimension.js"

const { Option } = Select;

export default function AddGlobalDimension(props) {
    const [form] = Form.useForm();
    const [linkedDimension, setLinkedDimension] = useState([])
    const [globalDimension, setGlobalDimension] = useState([])
    const [dimensions, setDimensions] = useState(null)
    const [selectedDimension, setSelectedDimension] = useState([])
    useEffect(()=>{
      if(props && props.linkedDimension){
        setLinkedDimension(props.linkedDimension)
      }
      if(!dimensions){
        getDimension()
      }
      
    }, []);

    const getDimension = async () => {
        const response = await globalDimensionService.getDimensions()
        setDimensions(response)
    }

    const onSelectChange = value => {
      setSelectedDimension(value)
    }

    const addGlobalDimensionFormSubmit = async (values) => {
        let payload = {
        };
        let dimensionalValues = []
        dimensionalValues = values["dimension"].map((value)=> {
          let temp = value.split(".");
          return {
            "datasetId":temp[0],
            "dataset":temp[1],
            "dimension":temp[2],
        }})
        payload["name"] = values["name"]
        payload["dimensionalValues"] = dimensionalValues 
        

        const response = await globalDimensionService.AddGlobalDimension(payload)
        if(response.success){
            props.onAddGlobalDimensionSuccess()
        }
        else{
            message.error(response.message);
        }
      };

    let dimensionForSuggestion = []
    dimensionForSuggestion = dimensions && dimensions.map(item =>(<Option value={item["datasetId"] + "." + item["dataset"]+ "." + item["dimension"]} key={item["dataset"] + "." + item["dimension"] } > {item["dataset"] + "." + item["dimension"]} </Option>))
   let dimensionOptions = []
   dimensionForSuggestion =
      dimensionForSuggestion &&
      dimensionForSuggestion.filter(
        item =>
          !linkedDimension.some(
            item1 => item && item.key === item1
          )
      );
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