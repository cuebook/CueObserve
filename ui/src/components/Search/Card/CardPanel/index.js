import React, { useState, useEffect, useRef } from "react";
import { message, Select, Table } from "antd";

import _ from "lodash";

import style from "./style.module.scss";

import TableCard from "components/Search/Card/Table";

export default function CardPanel(props) {

	if (_.isEmpty(props.cardData)){
		return <p>Please Go Back - ICON</p>
	}

	const data = props.cardData.data
	const title = props.cardData.title
	const text = props.cardData.text

	return (
		<div>
			<div className="flex">
			<div className={`w-9/12 ${style.chartPanel}`}>
			  <div className={style.anomalyTitle} dangerouslySetInnerHTML={{ __html: title }} />
			  <div className={style.anomalyText} dangerouslySetInnerHTML={{ __html: text }} />
			  <div className={style.chartDiv}> <TableCard data={data} /> </div>
			</div>
			</div>			
		</div>
		)
}
