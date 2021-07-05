import React, { useState, useEffect, useRef } from "react";
import style from "./style.module.scss";
import { useParams, useHistory } from 'react-router-dom';
import AceEditor from "react-ace";
import "ace-builds/src-noconflict/mode-mysql";
import "ace-builds/src-noconflict/theme-xcode";
import "ace-builds/src-noconflict/ext-language_tools";
import { Resizable } from "re-resizable";
import { message } from "antd"
import _ from "lodash";

import { Form, Button, Input,
  Radio,
  Select,
  Cascader,
  DatePicker,
  InputNumber,
  TreeSelect,
  Switch,
  Table
 } from 'antd';
import datasetService from "services/datasets";
import queryService from "services/querys";
import SelectConnection from "components/Connections/SelectConnection";

const { Option } = Select;

export default function Dataset(props) {
  const [datasetDetails, setDatasetDetails] = useState({})
  const [datasetName, setDatasetName] = useState("");
  const [datasetSql, setDatasetSql] = useState("");
  const [datasetConnection, setDatasetConnection] = useState(null);

  const [queryData, setQueryData] = useState(null)
  const [loadingQueryData, setLoadingQueryData] = useState(false)
  const [datasetColumns, setDatasetColumns] = useState([])
  const [datasetColumnType, setDatasetColumnType] = useState({})
  const [datasetGranularity, setDatasetGranlarity] = useState(null)

  const [isDataReceived, setIsDataReceived] = useState(false);
  const params = useParams()
  const history = useHistory();

  useEffect(()=>{
    if (params.datasetId && !isDataReceived){
      getDataset();
    }
  }, []);

  const getDataset = async () => {
    const data = await datasetService.getDataset(params.datasetId)
    if (data){
      setIsDataReceived(true);
      setDatasetName(data.name);
      setDatasetSql(data.sql);
      setDatasetConnection(data.connection.id);
      setDatasetGranlarity(data.granularity);
      setDatasetDetails(data);

      const tempColumnTypes = {}
      data.metrics && data.metrics.forEach(col=>{tempColumnTypes[col]="metric"})
      data.dimensions && data.dimensions.forEach(col=>{tempColumnTypes[col]="dimension"})
      tempColumnTypes[data.timestampColumn] = "timestamp"

      setDatasetColumnType(tempColumnTypes)
      let columns = data.metrics.concat(data.dimensions).concat([data.timestampColumn])
      columns = columns.sort()
      setDatasetColumns(columns)
    } 
  }

  const saveDataset = async () => {
    const metrics = Object.keys(datasetColumnType).filter(col=>datasetColumnType[col]=="metric")
    const dimensions = Object.keys(datasetColumnType).filter(col=>datasetColumnType[col]=="dimension")
    const timestamps = Object.keys(datasetColumnType).filter(col=>datasetColumnType[col]=="timestamp")

    if (!timestamps.length || timestamps.length > 1){
      message.error("Please select one timestamp column")
      return 
    }

    if (!datasetGranularity){
      message.error("Please select granularity")
      return 
    }

    const payload = {
      name: datasetName,
      sql: datasetSql,
      connectionId: datasetConnection,
      metrics: metrics,
      dimensions: dimensions,
      timestamp: timestamps[0],
      granularity: datasetGranularity,
    }
    if (params.datasetId)
      await datasetService.updateDataset(params.datasetId, payload)
    else {
      const response = await datasetService.createDataset(payload)
      if (response)
        history.push("/datasets")
    }
  }


  const runDatasetQuery = async () => {
    if (!datasetSql || !datasetConnection){
      message.error("Please select a connection & enter sql")
      return 
    }
    const payload = {
      sql: datasetSql,
      connectionId: datasetConnection
    }
    setLoadingQueryData(true)
    const data = await queryService.runQuery(payload)
    setLoadingQueryData(false)
    if (data && data.length){
      setQueryData(data)
      mergeColumns(Object.keys(data[0]))
    }
  }

  const mergeColumns = newColumns => {
    newColumns = newColumns.sort()
    const tempColumnType = datasetColumnType

    // remove removed columns
    datasetColumns.filter(col=>!newColumns.includes(col)).forEach(col=>{
      delete tempColumnType[col]
    })

    // add new columns
    newColumns.filter(col=>!datasetColumns.includes(col)).forEach(col=>{
      tempColumnType[col] = "metric"
    })
    setDatasetColumnType(tempColumnType)
    setDatasetColumns( newColumns )
  }

  const columns = datasetColumns.map(col=>{return {title: col, dataIndex: col, key: col }});  
  const queryDataTable = <Table columns={columns} dataSource={queryData} pagination={false} size="small" bordered={true} />


  const radioOptions = [{ label: 'Measure', value: 'metric' },
                        { label: 'Dimension', value: 'dimension' },
                        { label: 'Timestamp', value: 'timestamp' }]

  const typeSelectorColumns = [
    {
      title: "Column Name", 
      dataIndex: "name", 
      key: "name", 
      render: (text, record)=> {
        return record
      }
    }, 
    {
      title: "Column Type", 
      dataIndex: "action", 
      key: "action",
      align: "right",
      render: (text, record) => {
        return <Radio.Group
            options={radioOptions}
            onChange={e=>{setDatasetColumnType({...datasetColumnType, [record]: e.target.value})}}
            value={datasetColumnType[record]}
          />
      }
    }
  ]
  const selectFieldTypeTable = <Table columns={typeSelectorColumns} dataSource={datasetColumns} pagination={false} size="small" />

  return (
    <>
      <div className="col-5">
      <div className={`${style.dataset} col-5`}>
        <div className={style.datasetName}>
          <Input className={style.nameInput} placeholder="Enter Dataset name" onChange={e=>setDatasetName(e.target.value)} value={datasetName}/>
        </div>
        <div className={style.selectConnection}>
          <SelectConnection value={datasetConnection} onChange={setDatasetConnection} />
        </div>
        <div className={style.SQLEditor}>
          <SQLEditor value={datasetSql} setValue={setDatasetSql}/>
        </div>
        {
          queryData && queryData.length ? 
            <div className={style.dataTable}>
              {queryDataTable}
            </div> : null
        }
        {
          !datasetColumns.length ? null :
            <>
              <div className={style.typeSelectorTable}>
                <p>Select type for columns: </p>
                {selectFieldTypeTable}
              </div>
              <div className={style.granularity}>
                <p>Granularity: </p>
                    <Select style={{ width: 120 }} placeholder="Select granularity" value={datasetGranularity} onChange={setDatasetGranlarity}>
                      <Option value="hour">Hour</Option>
                      <Option value="day">Day</Option>
                      <Option value="week">Week</Option>
                    </Select>
              </div>
            </>
        }
        <div className={style.buttons}>
          <div className={style.run}>
            <Button type="primary" onClick={runDatasetQuery} loading={loadingQueryData}>Run SQL</Button>
          </div>
          { params.datasetId && datasetDetails.anomalyDefinitionCount ? null 
            :
          <div className={style.save}>
            <Button type="primary" onClick={saveDataset} disabled={queryData && queryData.length ? false : true }>Save Dataset</Button>
          </div>
          }
        </div>
      </div>   
      </div>

    </>
  );

}


export function SQLEditor(props){
  const [name, setName] = useState([]);
  var editorComponent;

  const resizerStyle = {
    border: "solid 1px #ddd",
    background: "#f0f0f0",
    zIndex: "1"
  };


  const complete = (editor, sqlSuggestionsList) => {
    const completers = sqlSuggestionsList.map(item => ({
      name: item,
      value: item,
      score: 100,
      meta: ""
    }));
    addCompleters(editor, completers); // The first argument is the reference entity and the second is the completion array
    // editor.completers.push(completers);
  };

  const addCompleters = (editor, completers, completersNew) => {
    if (completersNew) {
      // If the new completion is passed in, the previous completion will be blanked and the new content added.
      const arr = [];
      editor.completers = arr;
      editor.completers.push({
        getCompletions(editor, session, pos, prefix, callback) {
          callback(null, completers);
        }
      });
      return;
    }
    editor.completers.push({
      // first load loads all completions by default
      getCompletions(editor, session, pos, prefix, callback) {
        callback(null, completers);
      }
    });
  };


  const getKeywordsForSuggestion = cuelOptions => {
    let suggestionList = ["__time"];
    if (cuelOptions.datasource) {
      suggestionList.push(cuelOptions.datasource);
    }
    if (cuelOptions.datasource) {
      suggestionList.push(...cuelOptions.dimensions);
    }
    if (cuelOptions.datasource) {
      suggestionList.push(
        ...cuelOptions.metrics.filter(m => _.isNil(m.id)).map(m => m.name)
      );
    }
    return suggestionList;
  };

  return (
    <Resizable
      style={resizerStyle}
      defaultSize={{
        width: "auto",
        height: 200
      }}
      onResizeStop={() => {
        if (editorComponent) editorComponent.editor.resize();
      }}
    >
      <AceEditor
        mode="mysql"
        theme="xcode"
        onChange={val => props.setValue(val)
        }
        placeholder="SELECT * FROM TABLE"
        name="UNIQUE_ID_OF_DIV"
        value={props.value}
        key={"datasetSql"}
        // onLoad={x =>
        //   complete(
        //     x,
        //     getKeywordsForSuggestion({datasource: "", dimensions: [], metrics: []})
        //   )
        // }
        ref={el => (editorComponent = el)}
        width="100%"
        height="100%"
        readOnly={false}
        wrapEnabled={true}
        showPrintMargin={false}
        highlightActiveLine={true}
        setOptions={{
          enableBasicAutocompletion: true,
          enableLiveAutocompletion: true,
          enableSnippets: true,
          showLineNumbers: true,
          tabSize: 2
        }}
        // editorProps={{ $blockScrolling: true }}
      />
    </Resizable>
  )
}