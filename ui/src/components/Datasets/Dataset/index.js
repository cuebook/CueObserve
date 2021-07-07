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
import { calculateColumnsWidth } from "components/Utils/columnWidthHelper";

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
  const [viewOnlyMode, setViewOnlyMode] = useState(false)

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

      if (params.datasetId && data.anomalyDefinitionCount) setViewOnlyMode(true);

      const tempColumnTypes = {}
      data.metrics && data.metrics.forEach(col=>{tempColumnTypes[col]="metric"})
      data.dimensions && data.dimensions.forEach(col=>{tempColumnTypes[col]="dimension"})
      tempColumnTypes[data.timestampColumn] = "timestamp"

      setDatasetColumnType(tempColumnTypes)
      let columns = data.metrics.concat(data.dimensions).concat([data.timestampColumn])
      setDatasetColumns(columns)
      console.log(columns)
    } 
  }

  const saveDataset = async () => {
    const metrics = Object.keys(datasetColumnType).filter(col=>datasetColumnType[col]=="metric")
    const dimensions = Object.keys(datasetColumnType).filter(col=>datasetColumnType[col]=="dimension")
    const timestamps = Object.keys(datasetColumnType).filter(col=>datasetColumnType[col]=="timestamp")

    if (!datasetName) {
      message.error("Please enter name")
      return 
    }

    if (!datasetConnection) {
      message.error("Please select connection")
      return 
    }

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
      mergeColumns(data[0])
    }
  }

  const mergeColumns = columnValue => {
    const newColumns = Object.keys(columnValue)
    const tempColumnType = datasetColumnType

    // remove removed columns
    datasetColumns.filter(col=>!newColumns.includes(col)).forEach(col=>{
      delete tempColumnType[col]
    })

    // add new columns with datatype
    newColumns.filter(col=>!datasetColumns.includes(col)).forEach(col=>{
      tempColumnType[col] = columnValue[col] === parseInt(columnValue[col], 10) ? "metric" : "dimension";
    })

    setDatasetColumnType(tempColumnType)
    setDatasetColumns( newColumns )
  }

  const columns = datasetColumns.map(col=>{return {title: col, dataIndex: col, key: col }});  

  const dataTable = queryData && queryData.length && columns.length ? calculateColumnsWidth(columns, queryData , 400) : {}
  const queryDataTable = <Table className={style.antdTable} columns={queryData ? dataTable.columns : columns} dataSource={queryData ? dataTable.source : queryData} pagination={false} size="small" bordered={true} scroll={{ x: queryData ? 1200 : dataTable.tableWidth, y: 450 }} />

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
      dataIndex: "name", 
      key: "action",
      align: "right",
      render: (name, record) => {
        // let value = dataTable.columns.filter(c=>c.title==name)[0].align == "left" ? "dimension" : "metric"
        return <Radio.Group
            options={radioOptions}
            disabled={viewOnlyMode}
            onChange={e=>{setDatasetColumnType({...datasetColumnType, [record]: e.target.value})}}
            value={datasetColumnType[record]}
          />
      }
    }
  ]
  const selectFieldTypeTable = <Table columns={typeSelectorColumns} dataSource={datasetColumns} pagination={false} size="small" />

  return (
    <>
      <div className={`xl:w-9/12 ${style.dataset}`}>
        <div className={`lg:w-6/12 ${style.datasetName}`}>
          <Input className={`${style.nameInput}`} placeholder="Enter Dataset name" onChange={e=>setDatasetName(e.target.value)} value={datasetName}/>
        </div>
        <div className={style.selectConnection}>
          <SelectConnection value={datasetConnection} disabled={ viewOnlyMode } onChange={setDatasetConnection} />
        </div>
        <div className={style.SQLEditor}>
          <SQLEditor value={datasetSql} disabled={ viewOnlyMode } setValue={setDatasetSql}/>
        </div>
        <div className={style.buttons}>
          <div className={style.run}>
            <Button type="primary" onClick={runDatasetQuery} loading={loadingQueryData}>Run SQL</Button>
          </div>
        </div>
        <div className={`compact-table ${style.dataTable}`}>
          {queryDataTable}
        </div>
        {
          !datasetColumns.length ? null :
            <>
              <div className={`xl:w-8/12 ${style.typeSelectorTable}`}>
                <p>Select type for columns: </p>
                {selectFieldTypeTable}
              </div>
              <div className={style.granularity}>
                <p>Granularity: </p>
                    <Select style={{ width: 120 }} placeholder="Select granularity" value={datasetGranularity} onChange={setDatasetGranlarity} disabled={viewOnlyMode} >
                      <Option value="hour">Hour</Option>
                      <Option value="day">Day</Option>
                    </Select>
              </div>
            </>
        }
        <div className={style.buttons}>
          <div className={style.save}>
            <Button type="primary" onClick={saveDataset} disabled={ viewOnlyMode || !(queryData && queryData.length) }>Save Dataset</Button>
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
        readOnly={props.disabled ? props.disabled : false}
        disabled={true}
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