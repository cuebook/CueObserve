import React, { useState, useEffect, useRef } from "react";
import { Button, Form, Input, Switch, message, Select } from "antd";
import style from "./style.module.scss";

import globalDimensionService from "services/search/globalDimension.js"

const { Option } = Select;

export default function EditGlobalDimension(props) {
    const [form] = Form.useForm();
    const [linkedDimension, setLinkedDimension] = useState([])
    const [dimensions, setDimensions] = useState(null)
    const [selectedDimension, setEditSelectDimension] = useState()
    useEffect(()=>{
      if(props && props.linkedDimension){
        setLinkedDimension(props.linkedDimension)
        getGlobalDimensionById(props.editDimension.id)  
      }
      if(!dimensions){
        getDimension()
            }
    }, []);

    const getGlobalDimensionById = async (id) => {
        const response = await globalDimensionService.getGlobalDimension(id)
        let values = response.values.map((item)=>item["datasetId"]+"."+item["dataset"]+"."+item["dimension"])
        let linkedDimension = response.values.map((item)=>item["dataset"]+"."+item["dimension"])
        let name = response["name"]
        let dict = {}
        dict["name"] = response["name"]
        dict["selectLinkedDimension"] = linkedDimension
        dict["id"] = response["id"]
        dict["published"] = response["published"]
        dict["selectValues"] = values
        setEditSelectDimension(dict)
    }

    const getDimension = async () => {
        const response = await globalDimensionService.getDimensions()
        setDimensions(response)
    }

    const onSelectChange = value => {
    }

    const editGlobalDimensionFormSubmit = async (values) => {
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
        payload["id"] = selectedDimension && selectedDimension.id
        payload["dimensionalValues"] = dimensionalValues 
        payload["published"] = selectedDimension && selectedDimension.published

        const response = await globalDimensionService.editGlobalDimension(payload["id"], payload)
        if(response.success){
            props.onEditGlobalDimensionSuccess()
        }
        
      };

    const initialName = selectedDimension && selectedDimension.name
    const initialSelectedValue = selectedDimension && selectedDimension.selectValues
    // selectedLinkedDimension : Dimension that is linked with current editing global dimension
    const selectedLinkedDimension = selectedDimension && selectedDimension.selectLinkedDimension 
    let dimensionForSuggestion = []
    let linkedDimensionArray = []
    let addGlobalDimensionFormElement=[]
    if(selectedDimension){
      // linkedDimension are all ready linked with other global dimension
      // Just below line is for removing selectedLinkedDimension from linkedDimension to selectedLinkedDimension visible in select suggestion
    linkedDimensionArray = linkedDimension && linkedDimension.filter(item => !selectedLinkedDimension.some( item1 =>item && item == item1))

    dimensionForSuggestion = dimensions && dimensions.map(item =>(<Option value={item["datasetId"] + "." + item["dataset"]+ "." + item["dimension"]} key={item["dataset"] + "." + item["dimension"] } > {item["dataset"] + "." + item["dimension"]} </Option>))
   let dimensionOptions = []
   dimensionForSuggestion =
      dimensionForSuggestion &&
      dimensionForSuggestion.filter(
        item =>
          !linkedDimensionArray.some(
            item1 => item && item.key === item1
          )
      );
    let addGlobalDimensionParamElements = []

     addGlobalDimensionFormElement = (
      <div>
        <Form 
            layout="vertical" 
            className="mb-2" 
            form={form} 
            onFinish={editGlobalDimensionFormSubmit}
            name="addSchedule"
            scrollToFirstError
            hideRequiredMark
        >
          <div className={style.addConnectionForm}>
            <div className={style.formItem} style={{ width: "100%" }}>

            <Form.Item hasFeedback name="name" initialValue={initialName} rules={[{ required: true, message: 'Please input Global Dimension name!',whitespace: true }]}>
                <Input className={style.inputArea} placeholder={"Global Dimension Name"}/>
              </Form.Item>
            <Form.Item name ="dimension"  initialValue={initialSelectedValue} >
              <Select showSearch  mode="tags" style={{width: "100%"}} placeholder="Select Dimension" onChange={onSelectChange} >
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
                Save Global Dimension
            </Button>
          </div>
        </Form>
      </div>
    );
    }


    return (
      <div>
        <div className="row">
            <div>
              {selectedDimension? addGlobalDimensionFormElement : null}
            </div>
          
        </div>
      </div>
    );
}