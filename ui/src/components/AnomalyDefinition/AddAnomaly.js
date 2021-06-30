import React, { useState, useEffect } from "react";
import style from "./style.module.scss";
import { components } from "react-select";
import CreatableSelect from "react-select/creatable";
// import { connect } from "react-redux";
import { Modal, Select, Spin, Switch, Button, Radio, notification } from "antd";

const { Option } = Select;

let options = [];
let allOptions = {};
const operationMap = {
  daily: "day",
  "7day": "7day"
};

function generateOptions(autoCueOptions) {
  options = [];
  allOptions = {};

  if (autoCueOptions.queryTypes && autoCueOptions.queryTypes.length) {
    allOptions.operations = [];
    autoCueOptions.queryTypes.forEach(q => {
      if (operationMap[q]) {
        options.push({
          value: operationMap[q],
          label: q,
          optionType: "Operation",
          color: "#ff6767"
        });
        allOptions.operations.push({
          value: operationMap[q],
          label: q,
          optionType: "Operation",
          color: "#ff6767"
        });
      }
    });
  }

  if (autoCueOptions.globalMeasures && autoCueOptions.globalMeasures.length) {
    allOptions.metric = [];
    autoCueOptions.globalMeasures.forEach(q => {
      allOptions.metric.push({
        value: q,
        label: q.name,
        optionType: "Measure",
        color: "#ffc71f"
      });
    });
  }

  allOptions.dimension = [];
  if (autoCueOptions.dimensions && autoCueOptions.dimensions.length) {
    autoCueOptions.dimensions.forEach(q => {
      allOptions.dimension.push({
        value: q,
        label: q,
        optionType: "Dimension",
        color: "#12b1ff"
      });
    });
  }

  allOptions.segments = [];
  if (autoCueOptions.segments && autoCueOptions.segments.length) {
    autoCueOptions.segments.forEach(q => {
      allOptions.segments.push({
        value: q.origin + q.id,
        label: q.name,
        optionType: q.origin == "gd" ? "Global Dim Segment" : "Measure Segment",
        color: "#f241ff"
      });
    });
  }

  allOptions.highOrLow = [
    {
      value: "high",
      label: "Highs Only",
      optionType: "High Or Low",
      color: "#02c1a3"
    },
    {
      value: "low",
      label: "Lows Only",
      optionType: "High Or Low",
      color: "#02c1a3"
    }
  ];

  allOptions.contribution = [
    {
      value: "contribution",
      label: "On % Contribution",
      optionType: "Contribution",
      color: "#02c1a3"
    }
  ];

  allOptions.cardless = [
    {
      value: "cardless",
      label: "Cardless",
      optionType: "Cardless",
      color: "#02c1a3"
    }
  ];
}

function updateHelpText(selectedOption) {
  let elements = document.getElementsByClassName("autocue-help");
  while (elements.length > 0) {
    elements[0].parentNode.removeChild(elements[0]);
  }
  if (selectedOption) {
    setTimeout(function() {
      let elements = document.getElementsByClassName("autoCueOptions");
      let element = elements[elements.length - 1];
      let helpText = getHelpText(selectedOption);
      if (element)
        element.innerHTML +=
          "<span class='autocue-help'>" + helpText + "</span>";
    }, 150);
  }
}

const granularityKeyWords = ["day", "7day"];

function getOperationHelpText(value) {
  if (granularityKeyWords.indexOf(value) !== -1) {
    options = allOptions.metric;
    return " COUNT by STATE Lows Only";
  }
}

function getMetricHelpText(value, opts) {
  if (granularityKeyWords.indexOf(opts[0].value) !== -1) {
    options = [
      ...allOptions.dimension,
      ...allOptions.segments,
      ...allOptions.highOrLow
    ];
    return " by STATE";
  }
}

function getDimensionHelpText(value, opts) {
  if (granularityKeyWords.indexOf(opts[0].value) !== -1) {
    options = [];
    if (opts[1].value.measureClass == "Physical") {
      options = allOptions.contribution;
    }
    options = [...options, ...allOptions.highOrLow, ...allOptions.cardless];
    return " Highs Only";
  }
}

function getHelpText(selectedOption) {
  if (selectedOption && selectedOption.length) {
    let length = selectedOption.length;
    let lastOption = selectedOption[length - 1];
    let text = "";
    switch (lastOption.optionType) {
      case "Operation":
        text = getOperationHelpText(lastOption.value);
        break;
      case "Measure":
        text = getMetricHelpText(lastOption.value, selectedOption);
        break;
      case "High Or Low":
        options = allOptions.cardless;
        break;
      case "Dimension":
        text = getDimensionHelpText(lastOption.value, selectedOption);
        break;
      case "Global Dim Segment":
        text = getDimensionHelpText(lastOption.value, selectedOption);
        break;
      case "Measure Segment":
        text = getDimensionHelpText(lastOption.value, selectedOption);
        break;
      case "Contribution":
        options = allOptions.cardless;
        break;
      case "Cardless":
        options = [];
        break;
    }
    return text;
  }
  return "";
}

export default function AddAnomaly(){
  const [allDatasets, setAllDatasets] = useState([]);
  const [selectedDataset, setSelectedDataset] = useState([]);
  const [connections, setConnections] = useState([]);
  const [selectedOption, setSelectedOption] = useState([]);
  const [addingAnomaly, setAddingAnomaly] = useState([false]);
  const [datasetId, setDatasetId] = useState([]);
  const [cube_id, setCube_id] = useState([]);
  const [published, setPublished] = useState([]);
  const [isFocused, setIsFocused] = useState([false]);





  // constructor() {
    // super();
    // this.state = {
    //   selectedOption: null,
    //   addingAnomaly: false,
    //   published: false,
    //   cube_id: null
    // };
  // }

//   componentDidMount() {
//     const { dispatch } = this.props;
//     dispatch({
//       type: "cubes/LOAD_CUBES"
//     });
//     dispatch({
//       type: "cubes/GLOBAL_CUBE"
//     });
//     dispatch({
//       type: "cubes/GET_ANOMALYS"
//     });
//   }

  // componentWillReceiveProps(props) {
  //   generateOptions(props.query.autoCueOptions);
  // };

 const handleAddAnomaly = () => {
    const { dispatch } = this.props;
    const { selectedOption } = this.state;

    if (selectedOption.length < 2) {
      notification.warning(
        "Granularity and GlobalMeasure required to configure anomaly"
      );
      return;
    }

    var payload = {
      cube_id: cube_id,
      globalMeasure: selectedOption[1].value,
      granularity: selectedOption[0].value,
      published: published,
      highOrLow: ""
    };

    selectedOption.forEach(item => {
      if (item.optionType === "Cardless") {
        payload.cardless = true;
      }
      if (item.optionType === "Contribution") {
        payload.contribution = true;
      }
      if (item.optionType === "High Or Low") {
        payload.highOrLow = item.value;
      }
      if (item.optionType === "Dimension") {
        payload.dimension = item.value;
      }
      if (item.optionType === "Global Dim Segment") {
        payload.globalDimensionSegment = parseInt(item.value.substr(2));
      }
      if (item.optionType === "Measure Segment") {
        payload.measureSegment = parseInt(item.value.substr(2));
      }
    });

    // dispatch({
    //   type: "cubes/ADD_ANOMALY",
    //   payload: payload
    // });

    // this.setState({
    //   addingAnomaly: false,
    //   selectedOption: null
    // });
    // dispatch({
    //   type: "cubes/GET_ANOMALYS"
    // });
  };

 const handleCubeChange = value => {
    const { dispatch } = this.props;
    // dispatch({
    //   type: "query/LOAD_AUTO_CUE_OPTIONS",
    //   payload: value
    // });
    this.setState({ selectedOption: null, cube_id: value });
  };

  const handleChange = selectedOption => {
    const { dispatch } = this.props;
    // dispatch({
    //   type: "query/SET_STATE",
    //   payload: { autoCueQuery: selectedOption }
    // });
    this.setState({ selectedOption, isFocused: false });
    // updateOptions(selectedOption);
    updateHelpText(selectedOption);
    setTimeout(() => {
      this.setState({ isFocused: true });
    }, 200);
  };

  const  singleOption = props => {
    if (props.label.indexOf("Create ") !== -1) {
      return (
        <components.Option {...props}>
          <div className={style.optionWrapper}>
            <span className={style.subText}>{props.data.optionType}</span>
            <p style={{ color: props.data.color }} className={style.option}>
              {props.value}
            </p>
          </div>
        </components.Option>
      );
    } else {
      return (
        <components.Option {...props}>
          <div className={style.optionWrapper}>
            <p style={{ color: props.data.color }} className={style.option}>
              {props.label}
            </p>
            <span className={style.subText}>{props.data.optionType}</span>
          </div>
        </components.Option>
      );
    }
  };

  const multiValue = props => {
    return (
      <components.MultiValue {...props}>
        <div style={{ background: "white" }}></div>
      </components.MultiValue>
    );
  };

  const  multiValueContainer = props => {
    return (
      <components.MultiValueContainer {...props}>
        <div
          className={`autoCueOptions ${style.selectedOption}`}
          style={{ color: props.data.color }}
        >
          {props.data.label}
        </div>
      </components.MultiValueContainer>
    );
  };

  const handleOnCancel = () =>{
    setAddingAnomaly(false)
    setSelectedOption("")
  }

  const handleIsFocused = (val) => {
    setIsFocused(val)
  }

  // render() {
    // const {
    //   cubes: { cubes, globalCube }
    // } = this.props;
    // var cubeOptions = [];
    // cubeOptions = cubes.map(cube => (
    //   <Option value={cube.id} key={cube.id}>
    //     {cube.name}
    //   </Option>
    // ));

    return (
      <div>
        <div style={{ float: "right", paddingBottom: "10px" }}>
          <Button
            icon="plus"
            type="primary"
            onClick={() => setAddingAnomaly(true)}
          >
            New Anomaly Definition
          </Button>
        </div>
        {addingAnomaly == true ? (
          <Modal
            title="Add Anomaly"
            width="50%"
            centered
            visible={true}
            key="addAnomalyModal"
            onOk={() =>handleAddAnomaly()}
            onCancel={handleOnCancel}
            footer={[
              <Button
                key="back"
                type="primary"
                onClick={() => handleAddAnomaly()}
              >
                Save
              </Button>,
              <Button
                key="addingAnomalyButton"
                onClick={handleOnCancel}
              >
                Cancel
              </Button>
            ]}
          >
            <div className="pb-4 ">
              <div className="pl-4">
                <Select
                  className="pb-2 mx-2 "
                  showSearch
                  style={{ width: 200, float: "left" }}
                  placeholder="Select a dataset"
                  optionFilterProp="children"
                  onChange={handleCubeChange}
                //   notFoundContent={
                //     this.props.cubes.loading ? <Spin size="small" /> : null
                //   }
                  filterOption={(input, option) =>
                    option.props.children
                      .toLowerCase()
                      .indexOf(input.toLowerCase()) >= 0
                  }
                >
                  {/* {cubeOptions} */}
                </Select>
              </div>
              <div>

              <CreatableSelect
                styles={{
                  indicatorSeparator: () => {}, // removes the "stick"
                  dropdownIndicator: defaultStyles => ({
                    ...defaultStyles,
                    "& svg": { display: "none" }
                  })
                }}
                isMulti
                value={selectedOption}
                className={`${style.filterEditor}`}
                onChange={handleChange}
                onFocus={()=>handleIsFocused(true)}
                onBlur={() => handleIsFocused(false)}
                menuIsOpen={isFocused}
                components={{
                  Option: singleOption,
                  MultiValue: multiValue,
                  MultiValueContainer: multiValueContainer
                }}
                options={options}
                placeholder={`DAILY COUNT by STATE `}
              />
            </div>
            </div>
            
          </Modal>
        ) : null}
      </div>
    );
  }
// }
