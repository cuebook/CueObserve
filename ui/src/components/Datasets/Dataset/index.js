import React, { useState, useEffect, useRef } from "react";
import style from "./style.module.scss";
import { useParams, useHistory } from 'react-router-dom';
import AceEditor from "react-ace";
import { Resizable } from "re-resizable";
import _ from "lodash";

import { Form, Button, Input,
  Radio,
  Select,
  Cascader,
  DatePicker,
  InputNumber,
  TreeSelect,
  Switch,
 } from 'antd';
import datasetService from "services/datasets";
import SelectConnection from "components/Connections/SelectConnection";

export default function Dataset(props) {
  const [datasetName, setDatasetName] = useState("");
  const [datasetSql, setDatasetSql] = useState("");
  const [datasetConnection, setDatasetConnection] = useState(null);
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
      setDatasetConnection(data.connection.id)
    } 
  }

  const saveDataset = async () => {
    const payload = {
      name: datasetName,
      sql: datasetSql,
      connectionId: datasetConnection
    }
    if (params.datasetId)
      await datasetService.updateDataset(params.datasetId, payload)
    else {
      const response = await datasetService.createDataset(payload)
      if (response)
        history.push("/datasets")
    }
  }

  const runDataset = async () => {
    const payload = {
      sql: datasetSql,
      connectionId: datasetConnection
    }
    // await datasetService.runDataset(payload)
  }


  return (
    <>
      <div className={style.dataset}>
        <div className={style.datasetName}>
          <Input className={style.nameInput} placeholder="Enter Dataset name" onChange={e=>setDatasetName(e.target.value)} value={datasetName}/>
        </div>
        <div className={style.selectConnection}>
          <SelectConnection value={datasetConnection} onChange={setDatasetConnection} />
        </div>
        <div className={style.SQLEditor}>
          <SQLEditor value={datasetSql} setValue={setDatasetSql}/>
        </div>
        <div className={style.buttons}>
          <div className={style.run}>
            <Button type="primary">Run SQL</Button>
          </div>
          <div className={style.save}>
            <Button type="primary" onClick={saveDataset}>Save Dataset</Button>
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
    console.log(editor, sqlSuggestionsList)
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
        showPrintMargin={true}
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