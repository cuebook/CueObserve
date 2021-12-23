import React, { useState, useEffect } from "react";
import { Collapse } from "antd";
import style from "./style.module.scss";
import TimeAgo from 'react-timeago'
import Moment from 'react-moment';

var moment = require("moment");
const { Panel } = Collapse;


export default function RCALogs(props){
	const logs = props.data.logs;

	const logsJSX = Object.keys(logs).reverse().map(key => {
		return <div className="flex">
			<span className="w-3/12"><strong>{key}</strong></span>
			<span className="w-9/12"><pre className="text-xs">{logs[key]}</pre></span>
		</div>
	})

	let formatedDiff;
	if (props.data.startTimestamp && props.data.endTimestamp){
	  const timeDiff = Math.round((new Date(props.data.endTimestamp) - new Date(props.data.startTimestamp))/1000)
	  formatedDiff =  moment.duration(timeDiff, "second").format("h [hrs] m [min] s [sec]", {trim: "both"});
	}

	let logsHeader = null
	if (props.data.status == "SUCCESS"){
		logsHeader = <>
				<strong>Logs</strong>
				<div className="text-xs">
					succeeded <TimeAgo date={props.data.endTimestamp} /> in {formatedDiff}
				</div>			
			</>
	}
	else if (props.data.status == "ERROR"){
		logsHeader = <>
				<strong>Logs</strong>
				<div className="text-xs">
					failed <TimeAgo date={props.data.endTimestamp} /> in {formatedDiff}
				</div>			
			</>
	}
	else if (props.data.status == "RUNNING"){
		logsHeader = <>
				<strong>Logs</strong>
				<div className="text-xs">
					started  <TimeAgo date={props.data.startTimestamp} />
				</div>			
			</>
	}
	else if (props.data.status == "ABORTED"){
		logsHeader = <>
				<strong>Logs</strong>
				<div className="text-xs">
					aborted  <TimeAgo date={props.data.endTimestamp} /> in {formatedDiff}
				</div>			
			</>
	}

	return (<> 
	  <Collapse defaultActiveKey={props.data.status == "RUNNING" ? ['1'] : null} bordered={false} >
	    <Panel header={logsHeader} key="1">
			{logsJSX}
	    </Panel>
	  </Collapse>
	</>)
}