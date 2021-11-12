import React, { useState, useEffect, useRef, useContext } from "react";

import { GlobalContext } from "layouts/GlobalContext"

// import style from "./style.module.scss";

import CardPanel from "components/Search/Card/CardPanel";

export default function CardPage(props) {

	const { searchCardData, updateSearchCardData } = useContext(GlobalContext)

	return (<div>
		<CardPanel cardData={searchCardData} />
	</div>)
}