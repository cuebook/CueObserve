/*eslint-disable*/
import { Button, Switch } from "antd";
import React, { useState, useEffect } from "react";
import { Link, Redirect } from "react-router-dom";
import style from "./style.module.scss";
import userService from "services/main/user"
import Admin from "layouts/Admin"
import Login from "components/System/User/Login/index"
import { LogoutOutlined } from '@ant-design/icons';

export default function Sidebar(props) {
  const [isLoggedOut, setIsLoggedOut] = useState(false)
  const [logoutEnable, setLogoutEnable] = useState(false)

  useEffect(() => {
    if (props) {
      let temp = props.authRequire ? props.authRequire : false
      setLogoutEnable(temp)
    }
  }, []);

  const signOut = () =>{
    props.Logout(true)
  }
  let urlPrefix = ""
  const menuItems = [
    {
      "label": "Anomalies",
      "path": "/anomalies",
      "icon": "fa-exclamation-triangle"
    },
    {
      "label": "Anomaly Definitions",
      "path": "/anomalyDefinitions",
      "icon": "fa-cog"
    },
    {
      "label": "Datasets",
      "path": "/datasets",
      "icon": "fa-table"
    },
    {
      "label": "Connections",
      "path": "/connections",
      "icon": "fa-plug"
    },
    {
      "label": "Schedules",
      "path": "/schedules",
      "icon": "fa-calendar"
    },
    {
      "label": "Settings",
      "path": "/settings",
      "icon": "fa-cogs"
    },

    {
      "label": "Global Dimension",
      "path": "/search/global-dimension",
      "icon": "fa-cube"
    },

    {
      "label": "Search Results",
      "path": "/search/result",
      "icon": "fa-search"
    },
  ]

  let menuElements = []

  menuItems.forEach(menuItem => {
    menuElements.push(
      <li className="items-center" key={menuItem.path}>
        <Link
          className={
            `${style.navLink} text-xs uppercase py-3 font-bold block ` +
            (window.location.href.indexOf(urlPrefix + menuItem.path) !== -1
              ? "text-blue-500 hover:text-blue-600"
              : "text-gray-800 hover:text-gray-600")
          }
          to={urlPrefix + menuItem.path}
        >
          <i
            className={
              "fas " + menuItem.icon + " mr-2 text-sm " +
              (window.location.href.indexOf(urlPrefix + menuItem.path) !== -1
                ? "opacity-75"
                : "text-gray-400")
            }
          ></i>{" "}
          <span className={props.isEmbedPage ? style.embedLabel : ""}>
            {menuItem.label}
          </span>
        </Link>
      </li>
    )
  })
  return (
    <>
      <nav className={`md:left-0 
            md:block md:fixed md:top-0 md:bottom-0 md:overflow-y-auto md:flex-row 
            md:flex-no-wrap md:overflow-hidden shadow-xl bg-white flex flex-wrap items-center 
            justify-between relative z-10 py-4 px-6 
            ${props.isEmbedPage ? style.embedNavBar : "md:w-64"}`
        }>
        <div className="md:flex-col md:items-stretch md:min-h-full md:flex-no-wrap px-0 flex flex-wrap items-center justify-between w-full mx-auto">
          { 
          props.isEmbedPage 
          ?
          null 
          :
          <>
            {/* Brand */}
            <Link
              className="md:block text-left md:pb-1 text-gray-700 mr-0 inline-block whitespace-no-wrap text-sm uppercase font-bold p-0 px-0"
              to={urlPrefix + "/"}
            >
              <img src={require("assets/img/cueObserve.png")} />
            </Link>
            </>
          }
          <div
            className={`md:flex md:flex-col md:items-stretch md:opacity-100 md:relative md:mt-2 md:shadow-none shadow absolute top-0 left-0 right-0 z-40 overflow-y-auto overflow-x-hidden h-auto items-center flex-1 rounded`}
          >
            { props.isEmbedPage ?
              null
            :
              <hr className="my-4 md:min-w-full" />
            }
            {/* Heading */}

            <ul className="md:flex-col md:min-w-full flex flex-col list-none">
              { menuElements }
            </ul>
          </div>
          {logoutEnable ? 
          <Button
            type="secondary"
            onClick={signOut}
            className={"uppercase font-bold text-gray-800 "}
            >
              <i className={"fas fa-sign-out-alt mr-2 text-sm text-gray-400 "}></i>
            SIGN OUT
          </Button>
          : ""} 
        </div>
      </nav>
    </>
  );
}
