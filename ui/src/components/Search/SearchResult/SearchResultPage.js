import React, { useState, useEffect, useRef } from "react";
// import { Helmet } from "react-helmet";
import { Switch, Table, Button, Input, Drawer, Affix } from 'antd';
import {EditOutlined } from '@ant-design/icons';
import style from "./style.module.scss";
import searchResultService from "services/search/searchResult.js"
// import TrackVisibility from "react-on-screen";

export default function SearchResultPage(props){
  const [searchCard, setSearchCard] = useState()
  const [searchPayload, setSearchPayload] = useState({})
  useEffect(()=>{
    if(!searchCard){
      //searchPayload will be calculated from url and pass it for further operations
      getSearchCard(searchPayload)
    }
  }, []);



  const getSearchCard = async (searchPayload) => {
    const response = await searchResultService.getSearchCards(searchPayload)
    if(response.success){
      console.log("response", response)
      setSearchCard(response.searchCards)
    }
  }

  let phantomCardsArray = []
  let cardsArray = []
  let loading = null
  let cardTypesArray = []
console.log("searchCars", searchCard)
if(searchCard){
  console.log("searchcard in if ", searchCard)
  cardsArray = searchCard && searchCard.map(item=>
    <div>
      {item.Title} + {item.Text}
    </div>
  )
}

console.log("cardsArray", cardsArray)

return (
        <div>
          <div className={`row ${style.searchResultsWrapper}`} >
            <div className="col-lg-7">
                {/* <h4>No results found.</h4> */}
              {cardsArray}
              
            </div>
          </div>
      </div>
    );

}