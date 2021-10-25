import React from "react";
import Search from "./Search";
// import UserMenu from "./UserMenu";
// import SubMenu from "./SubMenu";
import style from "./style.module.scss";
// import { history } from "index";
// import { connect } from "react-redux";
import { withRouter } from "react-router-dom";


// @withRouter
export default function TopBar (props) {

//  const searchSubmit = searchPayload => {
//     const searchQuery = encodeURIComponent(JSON.stringify(searchPayload));
//     history.push("/search?search=" + searchQuery);
//   };

//     const { user } = this.props;
//     let params = new URLSearchParams(this.props.location.search);
//     let initialSearchValue = [];
//     try {
//       let searchQuery = JSON.parse(params.get("search"));
//       initialSearchValue = searchQuery
//         ? [
//             {
//               label: searchQuery["names"].join(" "),
//               searchType: "PREVIOUSSEARCHPAYLOAD",
//               searchPayload: searchQuery
//             }
//           ]
//         : [];
//     } catch (error) {}

    return (
      <div className={style.topbar}>
          <div className={`col-lg-7 searchbar`}>
            <div style={{ marginRight: "-15px" }}>
              <Search
                // onSubmit={searchSubmit}
                // initialValue={initialSearchValue}
                // isSeachButtonVisible={true}
              />
            </div>
          </div>
      </div>
    );
  }

