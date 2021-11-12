import React, { useState, useEffect, useRef } from "react";
import { message, Select, Table } from "antd";

import style from "./style.module.scss";

import TableCard from "components/Search/Card/Table";

export default function CardPanel(props) {

	const data = [
	    {
	        "CREATEDTS": "2021-10-31T20:00:00.000Z",
	        "DeliveryCity": "Bangalore",
	        "DeliveryPostalCode": "560035",
	        "DeliveryRegionCode": "KA",
	        "BrandCode": "",
	        "ColorCode": "",
	        "WarehouseCode": "304",
	        "ReturnEntries": 1,
	        "ExpectedQty": 1,
	        "RefundAmount": 0,
	        "FinalReturnQty": 0,
	        "ReceivedQty": 0
	    },
	    {
	        "CREATEDTS": "2021-10-31T20:00:00.000Z",
	        "DeliveryCity": "Delhi",
	        "DeliveryPostalCode": "110068",
	        "DeliveryRegionCode": "DL",
	        "BrandCode": "",
	        "ColorCode": "",
	        "WarehouseCode": "110",
	        "ReturnEntries": 1,
	        "ExpectedQty": 1,
	        "RefundAmount": 0,
	        "FinalReturnQty": 0,
	        "ReceivedQty": 0
	    },
	    {
	        "CREATEDTS": "2021-10-31T20:00:00.000Z",
	        "DeliveryCity": "Faridabad",
	        "DeliveryPostalCode": "121003",
	        "DeliveryRegionCode": "HR",
	        "BrandCode": "",
	        "ColorCode": "",
	        "WarehouseCode": "130",
	        "ReturnEntries": 1,
	        "ExpectedQty": 1,
	        "RefundAmount": 0,
	        "FinalReturnQty": 0,
	        "ReceivedQty": 0
	    },
	    {
	        "CREATEDTS": "2021-10-31T20:00:00.000Z",
	        "DeliveryCity": "Kolkata",
	        "DeliveryPostalCode": "700089",
	        "DeliveryRegionCode": "WB",
	        "BrandCode": "GIORDANO",
	        "ColorCode": "NO COLOUR",
	        "WarehouseCode": "161",
	        "ReturnEntries": 1,
	        "ExpectedQty": 1,
	        "RefundAmount": 0,
	        "FinalReturnQty": 0,
	        "ReceivedQty": 0
	    },
	    {
	        "CREATEDTS": "2021-10-31T20:00:00.000Z",
	        "DeliveryCity": "Lucknow",
	        "DeliveryPostalCode": "226013",
	        "DeliveryRegionCode": "UP",
	        "BrandCode": "RARE",
	        "ColorCode": "NAVY",
	        "WarehouseCode": "305",
	        "ReturnEntries": 1,
	        "ExpectedQty": 1,
	        "RefundAmount": 0,
	        "FinalReturnQty": 0,
	        "ReceivedQty": 0
	    },
	    {
	        "CREATEDTS": "2021-10-31T19:00:00.000Z",
	        "DeliveryCity": "Delhi",
	        "DeliveryPostalCode": "110087",
	        "DeliveryRegionCode": "DL",
	        "BrandCode": "",
	        "ColorCode": "",
	        "WarehouseCode": "305",
	        "ReturnEntries": 1,
	        "ExpectedQty": 1,
	        "RefundAmount": 0,
	        "FinalReturnQty": 0,
	        "ReceivedQty": 0
	    },
	    {
	        "CREATEDTS": "2021-10-31T19:00:00.000Z",
	        "DeliveryCity": "Faridabad",
	        "DeliveryPostalCode": "121001",
	        "DeliveryRegionCode": "HR",
	        "BrandCode": "",
	        "ColorCode": "",
	        "WarehouseCode": "127",
	        "ReturnEntries": 1,
	        "ExpectedQty": 1,
	        "RefundAmount": 0,
	        "FinalReturnQty": 0,
	        "ReceivedQty": 0
	    },
	    {
	        "CREATEDTS": "2021-10-31T19:00:00.000Z",
	        "DeliveryCity": "Kolkata",
	        "DeliveryPostalCode": "700070",
	        "DeliveryRegionCode": "WB",
	        "BrandCode": "",
	        "ColorCode": "",
	        "WarehouseCode": "188",
	        "ReturnEntries": 1,
	        "ExpectedQty": 1,
	        "RefundAmount": 0,
	        "FinalReturnQty": 0,
	        "ReceivedQty": 0
	    },
	    {
	        "CREATEDTS": "2021-10-31T19:00:00.000Z",
	        "DeliveryCity": "Mumbai",
	        "DeliveryPostalCode": "400050",
	        "DeliveryRegionCode": "MH",
	        "BrandCode": "",
	        "ColorCode": "",
	        "WarehouseCode": "114",
	        "ReturnEntries": 1,
	        "ExpectedQty": 1,
	        "RefundAmount": 0,
	        "FinalReturnQty": 0,
	        "ReceivedQty": 0
	    },
	    {
	        "CREATEDTS": "2021-10-31T19:00:00.000Z",
	        "DeliveryCity": "Mumbai",
	        "DeliveryPostalCode": "400067",
	        "DeliveryRegionCode": "MH",
	        "BrandCode": "",
	        "ColorCode": "",
	        "WarehouseCode": "346",
	        "ReturnEntries": 1,
	        "ExpectedQty": 1,
	        "RefundAmount": 0,
	        "FinalReturnQty": 0,
	        "ReceivedQty": 0
	    }
	]

	const title = "Data for dataset xyz where CITY = DELHI"
	const text = "Data for dataset xyz where CITY = DELI"

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
