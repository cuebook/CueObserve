import React from "react";
import Search from "./Search";
// import UserMenu from "./UserMenu";
// import SubMenu from "./SubMenu";
import {useHistory} from "react-router-dom"
import style from "./style.module.scss";
// import { history } from "index";
// import { connect } from "react-redux";
import { withRouter } from "react-router-dom";



export default function TopBar (props) {
const history = useHistory()
 const searchSubmit = searchPayload => {
    const searchQuery = encodeURIComponent(JSON.stringify(searchPayload));
    history.push("/search?search=" + searchQuery);
  };

    // const { user } = this.props;
    let params = new URLSearchParams(history.location.search);
    let initialSearchValue = [];
    try {
      let searchQuery = JSON.parse(params.get("search"));
      initialSearchValue = searchQuery
        ? [
            {
              label: searchQuery["names"].join(" "),
              searchType: "PREVIOUSSEARCHPAYLOAD",
              searchPayload: searchQuery
            }
          ]
        : [];
    } catch (error) {}

    return (
      <div className={style.topbar}>
          <div className={`col-lg-7 searchbar`}>
            <div style={{ marginRight: "-15px" }}>
            <Search
                onSubmit={searchSubmit}
                initialValue={initialSearchValue}
                isSearchButtonVisible={true}
              />
            </div>
          </div>
      </div>
    );
  }

