import React from "react";
import { notification } from "antd";
// import StarRatings from "react-star-ratings";
// import { connect } from "react-redux";
import AsyncSelect from "react-select/async";
import { components } from "react-select";
import styles from "./style.module.scss";
import ApiService from "services/api";
import _ from "lodash";
import { Tag, Button } from "antd";
import { SearchOutlined } from "@ant-design/icons";
import SearchResultService from "services/search/searchResult.js"
// import AutosizeInput from "react-input-autosize";
// import { search } from "utilities/general";

const SearchTypeConstants = {
  ANOMALIES: "ANOMALIES",
  GLOBALDIMENSION: "GLOBALDIMENSION",
  MEASURE: "MEASURE",
  OPERATION: "OPERATION",
  DIMENSION: "DIMENSION",
  REGULAR: "REGULAR",
  TAG: "TAG",
  SEGMENT: "SEGMENT",
  PREVIOUSSEARCHPAYLOAD: "PREVIOUSSEARCHPAYLOAD",
  DRILLOBJECTFILTER: "DRILLOBJECTFILTER"
};

const formatOptionLabel = data => {
  const type = data.type ? data.type.trim() : null;
  let metadata;
  if (_.isNil(type) || type.length === 0) metadata = <div />;
  else if (type === SearchTypeConstants.ANOMALIES) metadata = <div />;
  else if (type === SearchTypeConstants.DIMENSION)
    metadata = <Tag color="green">{type}</Tag>;
  else if (type === SearchTypeConstants.MEASURE)
    metadata = <Tag color="red">{type}</Tag>;
  else metadata = <Tag color="blue">{type}</Tag>;

  //const metadata = (_.isNil(type) || type.length === 0) ? <div /> : <Tag color="blue">{type}</Tag>;
  return (
    <div className={`${styles.selectoptions} cueapp-search-options`}>
      {data.label}
      <span className={styles.selectoptionsRight}>{metadata}</span>
      </div>
  );
};

var valueInput = React.createRef();
var valueInput2 = React.createRef();

const MultiValueContainer = (props, data) => {
  let label = props.data.boxLabel ? props.data.boxLabel : props.data.label;
  if (props.data.type === SearchTypeConstants.OPERATION) {
    if (props.data.value1 === undefined) props.data.value1 = "";
  }
  return (
    <components.MultiValueContainer {...props}>
      <div className={`autoCueOptions cueapp-search selectedOption`}>
        {label}
        {/* The code below is for enabling filters for a dimension. Uncommnet when feature is ready from backend. */}
      </div>
    </components.MultiValueContainer>
  );
};

class Search extends React.Component {
  constructor(props) {
    super();
    this.state = {
      query: "",
      selectedGlobalDimensionItems: [],
      value: [],
      selectedEntries: [],
      searchPayload: {},
      menuIsOpen: false,
      searchSuggestions: []
    };
    this.searchInputRef = React.createRef();
    this.searchButtonRef = React.createRef();
    this.selectedEntries = props.initialValue ? props.initialValue : [];
  }

  getSearchSuggestions = async(searchQuery) => {
    // let apiService = new ApiService();

    return await SearchResultService.getSearchSuggestions(searchQuery)
      // .post("searchsuggestions/", {
      //   query: searchQuery,
      //   // datasource: this.props.datasource,
      //   // isCueDrill: this.props.isCueDrill,
      //   // cubeId: this.props.cubeId
      // })
      .then(res => {
        if (res.success && res.data) {
          let options = res.data.map(e => {
            return {
              ...e,
              value: e.value + "_" + e.user_entity_identifier,
              label: e.value,
              type: e.user_entity_identifier,
              searchType: e.type,
            };
          });

          let staticOptions = [
            {
              label: "See all results",
              value: searchQuery,
              type: ""
            }
          ];
          let opts = [...options];
          
          this.setState({ searchSuggestions: opts });
          return opts;
        }
      });
  };
  onChangeFilter = (selectedEntries, action) => {
    this.selectedEntries = selectedEntries;
    if (!_.isNil(selectedEntries)) {
      const e = selectedEntries[selectedEntries.length - 1];
      if (selectedEntries.length === 0) {
        this.setState({ ...this.state, selectedGlobalDimensionItems: [] });
      } else if (
        e.searchType === SearchTypeConstants.GLOBALDIMENSION ||
        e.searchType === SearchTypeConstants.MEASURE ||
        e.searchType === SearchTypeConstants.ANOMALIES ||
        e.searchType === SearchTypeConstants.DIMENSION ||
        e.searchType === SearchTypeConstants.OPERATION ||
        e.searchType === SearchTypeConstants.SEGMENT ||
        e.searchType === SearchTypeConstants.TAG
      ) {
        const selectedMeasures = selectedEntries
          .filter(e1 => e1.searchType === SearchTypeConstants.MEASURE)
          .map(e1 => {
            return {
              measureName: e1.value,
              cubeNames: e1.id
            };
          });

        if (selectedMeasures.length > 1) {
          notification.warning({
            message: "Multiple measures selected",
            description: "Multiple measures not supported in search",
            onClick: () => {}
          });
        }
      } else {
        // here means see all card results
        this.getSearchResults();
      }
    }
    if (action.action === "select-option") {
      this.setState({ query: "", selectedEntries: this.selectedEntries });
    }
    if (this.props.submitOnSelect) {
      this.getSearchResults();
    }
  };

  onInputChange = (event, reason) => {
    if (reason.action === "input-blur" || reason.action === "menu-close") {
      return;
    } else if (reason.action === "set-value") {
      this.setState({ query: "" });
    } else {
      if (document.activeElement !== valueInput) {
        this.setState({ query: event });
      }
    }
  };

  getFocusedOption() {
    return this.searchInputRef.select.select.state.focusedOption;
  }

  isMenuOpen() {
    return this.searchInputRef.select.state.menuIsOpen;
  }

  onUserInteracted = e => {
    if (e.key == "Backspace") {
      if (this.state.query == "") {
        if (
          this.selectedEntries.length > 0 &&
          this.selectedEntries[this.selectedEntries.length - 1].type ===
            SearchTypeConstants.OPERATION &&
          valueInput2 &&
          valueInput2.value
        ) {
          valueInput2.focus();
        } else if (
          this.selectedEntries.length > 0 &&
          this.selectedEntries[this.selectedEntries.length - 1].type ===
            SearchTypeConstants.OPERATION &&
          valueInput &&
          valueInput.value
        ) {
          valueInput.focus();
        } else if (this.selectedEntries.length) {
          this.selectedEntries.pop();
          this.setState({ selectedEntries: this.selectedEntries });
          this.searchInputRef.current.blur();
          setTimeout(() => {
            this.searchInputRef.current.focus();
          }, 200);
        }
      }
      if (this.props.isCueDrill) {
        this.getSearchResults();
      }
    } else if (e.key == "Enter") {
      if (document.activeElement === valueInput) {
        if (valueInput2 && valueInput2.type) {
          valueInput2.focus();
        } else {
          this.searchInputRef.current.focus();
        }
      } else if (document.activeElement === valueInput2) {
        this.searchInputRef.current.focus();
      }
      if (this.props.isCueDrill) {
        this.getSearchResults();
      }
    } else if (e.key == "Tab" && this.props.isSeachButtonVisible) {
      this.searchButtonRef.current.buttonNode.focus();
      e.preventDefault();
      e.stopPropagation();
    } else if (e.key == "ArrowLeft") {
      try {
        if (
          (document.activeElement === valueInput &&
            valueInput.selectionStart !== 0) ||
          (document.activeElement === valueInput2 &&
            valueInput2.selectionStart !== 0)
        ) {
          e.preventDefault();
          e.stopPropagation();
          document.activeElement.selectionStart -= 1;
          document.activeElement.selectionEnd =
            document.activeElement.selectionStart;
        }
      } catch (error) {}
    } else if (e.key == "ArrowRight") {
      try {
        if (
          (document.activeElement === valueInput &&
            valueInput.selectionStart !== valueInput.value.length) ||
          (document.activeElement === valueInput2 &&
            valueInput2.selectionStart !== valueInput2.value.length)
        ) {
          e.preventDefault();
          e.stopPropagation();
          document.activeElement.selectionStart += 1;
          document.activeElement.selectionEnd =
            document.activeElement.selectionStart;
        }
      } catch (error) {}
    }
  };

  getSearchResults = () => {
    // if (
    //   (this.selectedEntries && this.selectedEntries.length) ||
    //   this.state.query
    // ) {
    this.props.onSubmit(this.selectedEntries);
    // }
  };

  getBoundFilterName = boundFilter => {
    let name = boundFilter["operation"];
    if (boundFilter.value1) {
      name += " " + String(boundFilter["value1"]);
    }
    if (boundFilter.value2) {
      name += " and " + String(boundFilter["value2"]);
    }
    return name;
  };

  debouncedFetch = _.debounce((searchTerm, callback) => {
    this.getSearchSuggestions(searchTerm)
      .then(result => callback(null, { options: result }))
      .catch(error => callback(error, null));
  }, 300);

  onBlur = () => {
    this.setState({ menuIsOpen: false });
  };

  onFocus = () => {
    this.setState({ menuIsOpen: true });
  };

  render() {
    const DropdownIndicator = props => {
      return null;
    };
    return (
      <div className={`cueapp-search ${styles.topBarSearch}`}>
        <AsyncSelect
          ref={this.searchInputRef}
          cacheOptions
          defaultOptions
          loadOptions={this.getSearchSuggestions}
          closeMenuOnSelect={false}
          isMulti
          maxMenuHeight={638}
          components={{
            DropdownIndicator,
            MultiValueContainer,
            IndicatorSeparator: () => null
          }}
          onKeyDown={this.onUserInteracted}
          formatOptionLabel={formatOptionLabel}
          placeholder={
            this.props.placeholder ? this.props.placeholder : "Search"
          }
          onChange={(event, action) => this.onChangeFilter(event, action)}
          onFocus={this.onFocus}
          onBlur={this.onBlur}
          tabSelectsValue={false}
          menuIsOpen={
            this.state.menuIsOpen &&
            this.state.searchSuggestions.length &&
            this.state.query.length
          }
          onInputChange={(a, b) => {
            this.onInputChange(a, b);
          }}
          value={this.selectedEntries}
          backspaceRemovesValue={false}
          inputValue={this.state.query}
          
          menuPortalTarget={document.body} 
          styles={{ menuPortal: base => ({ ...base, zIndex: 9999 }) }}
          noOptionsMessage={() => {
            return <></>;
          }}
          id="search-box"
        />
        {this.props.isSearchButtonVisible ? (
          <div className={styles.searchBtnWrapper}>
            <Button
              type="primary"
              onClick={this.getSearchResults}
              className={styles.searchButton}
              ref={this.searchButtonRef}
              id="search-button"
            >
              <SearchOutlined alt="search-icon" />
            </Button>
          </div>
        ) : null}
      </div>
    );
  }
}

export default Search;
