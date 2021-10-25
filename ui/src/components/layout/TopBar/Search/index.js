import React from "react";
import { notification } from "antd";
import AsyncSelect from "react-select/async";
// import { components } from "react-select";
import styles from "./style.module.scss";
// import ApiService from "services/api";
import _ from "lodash";
import { Tag, Button } from "antd";
import { SearchOutlined } from "@ant-design/icons";
// import AutosizeInput from "react-input-autosize";
// import { search } from "utilities/general";


var valueInput = React.createRef();
var valueInput2 = React.createRef();


export default function Search () {
  //   super();
  //   this.state = {
  //     query: "",
  //     selectedGlobalDimensionItems: [],
  //     value: [],
  //     selectedEntries: [],
  //     searchPayload: {},
  //     menuIsOpen: false,
  //     searchSuggestions: []
  //   };
  //   this.searchInputRef = React.createRef();
  //   this.searchButtonRef = React.createRef();
  //   this.selectedEntries = props.initialValue ? props.initialValue : [];
  // }

  // onInputChange = (event, reason) => {
  //   if (reason.action === "input-blur" || reason.action === "menu-close") {
  //     return;
  //   } else if (reason.action === "set-value") {
  //     this.setState({ query: "" });
  //   } else {
  //     if (document.activeElement !== valueInput) {
  //       this.setState({ query: event });
  //     }
  //   }
  // };

  // getFocusedOption() {
  //   return this.searchInputRef.select.select.state.focusedOption;
  // }

  // isMenuOpen() {
  //   return this.searchInputRef.select.state.menuIsOpen;
  // }



  // getBoundFilterName = boundFilter => {
  //   let name = boundFilter["operation"];
  //   if (boundFilter.value1) {
  //     name += " " + String(boundFilter["value1"]);
  //   }
  //   if (boundFilter.value2) {
  //     name += " and " + String(boundFilter["value2"]);
  //   }
  //   return name;
  // };

  // debouncedFetch = _.debounce((searchTerm, callback) => {
  //   this.getSearchSuggestions(searchTerm)
  //     .then(result => callback(null, { options: result }))
  //     .catch(error => callback(error, null));
  // }, 300);

  // onBlur = () => {
  //   this.setState({ menuIsOpen: false });
  // };

  // onFocus = () => {
  //   this.setState({ menuIsOpen: true });
  // };

  // render() {
  //   const DropdownIndicator = props => {
  //     return null;
  //   };

    return (
      <div className={`cueapp-search ${styles.topBarSearch}`}>
        <AsyncSelect
          // ref={this.searchInputRef}
          cacheOptions
          defaultOptions
          // loadOptions={this.getSearchSuggestions}
          closeMenuOnSelect={false}
          isMulti
          maxMenuHeight={638}
          // components={{
          //   DropdownIndicator,
          //   MultiValueContainer,
          //   IndicatorSeparator: () => null
          // }}
          // onKeyDown={this.onUserInteracted}
          // formatOptionLabel={formatOptionLabel}
          placeholder={
             "Search"
          }
          // onChange={(event, action) => this.onChangeFilter(event, action)}
          // onFocus={this.onFocus}
          // onBlur={this.onBlur}
          tabSelectsValue={false}
          // menuIsOpen={
          //   this.state.menuIsOpen &&
          //   this.state.searchSuggestions.length &&
          //   this.state.query.length
          // }
          // onInputChange={(a, b) => {
          //   this.onInputChange(a, b);
          // }}
          // value={this.selectedEntries}
          backspaceRemovesValue={false}
          // inputValue={this.state.query}
          noOptionsMessage={() => {
            return <></>;
          }}
          id="search-box"
        />
        {/* {this.props.isSeachButtonVisible ? ( */}
          <div className={styles.searchBtnWrapper}>
            <Button
              type="primary"
              // onClick={this.getSearchResults}
              // className={styles.searchButton}
              // ref={this.searchButtonRef}
              id="search-button"
            >
              <SearchOutlined alt="search-icon" />
            </Button>
          </div>
        {/* ) : null} */}
      </div>
    );
  }

