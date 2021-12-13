import React, { useState, useEffect, useRef } from "react";
import { message, Select, Table } from "antd";
import _ from "lodash";

import { calculateColumnsWidth } from "components/Utils/columnWidthHelper";

import style from "./style.module.scss";

export default function TableCard(props) {
	const data = props.data
	const columns = !_.isEmpty(data) && Object.keys(data[0]).map(col=>{return {title: col, dataIndex: col, key: col }});  

	const styledTable = !_.isEmpty(data) ? calculateColumnsWidth(columns, data , 400) : {}

	const tableScroll = props.isSnippet ? {x: data ? 1200 : styledTable.tableWidth, y: 120} : {x: data ? 1200 : styledTable.tableWidth, y: 480}

	const dataTable = <Table className={style.antdTable} columns={columns} dataSource={data ? styledTable.source : data} pagination={false} size="xs" bordered={true} scroll={ tableScroll } />

	return (      
		<div className="cardTable">
			{ dataTable }
		</div>
    )
}