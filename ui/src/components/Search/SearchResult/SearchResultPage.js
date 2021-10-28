import React, { useState, useEffect, useRef } from "react";
// import { Helmet } from "react-helmet";
import { Switch, Table, Button, Input, Drawer, Affix } from 'antd';
import {EditOutlined } from '@ant-design/icons';
import style from "./style.module.scss";
import {useHistory} from "react-router-dom"
import searchResultService from "services/search/searchResult.js"
// import TrackVisibility from "react-on-screen";

export default function SearchResultPage(props){
  const history = useHistory()
  const [searchCard, setSearchCard] = useState()
  const [searchPayload, setSearchPayload] = useState()
  useEffect(()=>{
        getSearchCard()
  }, []);

  const getSearchPayloadFromUrl = () =>{
    let params = new URLSearchParams(history.location.search);
    let searchQuery = JSON.parse(params.get("search"));
    setSearchPayload(searchQuery)
  }

  const getSearchCard = async () => {
    let params = new URLSearchParams(history.location.search);
    let searchPayload = JSON.parse(params.get("search"));
    const response = await searchResultService.getSearchCards(searchPayload)
    if(response.success){
      setSearchCard(response.searchCards)
    }
  }

  let phantomCardsArray = []
  let cardsArray = []
  let loading = null
  let cardTypesArray = []

  // Below Code is Temporary 
if(searchCard){
  cardsArray = searchCard && searchCard.map(item=>
    <div key={item.Title}>
      {item.Title} + {item.Text}
    </div>
  )
}

console.log("cardsArray", cardsArray)

return (
        <div>
          <div className={`row ${style.searchResultsWrapper}`} >
            <div className="col-lg-7">
              {cardsArray.length > 0 ? null :(
                <h4>No results found.</h4>
                )}
              {cardsArray}
              
            </div>
          </div>
      </div>
    );

}