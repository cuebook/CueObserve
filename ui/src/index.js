import React from "react";
import ReactDOM from "react-dom";
import { HashRouter, Route, Switch, Redirect } from "react-router-dom";
import 'react-notifications-component/dist/theme.css'
import firebase from "firebase/compat/app"
import "@fortawesome/fontawesome-free/css/all.min.css";
import "assets/styles/tailwind.css";
import 'antd/dist/antd.css';

// firebase Telemetry
// layouts
import Admin from "layouts/Admin.js";
import {firebaseConfig} from "telemetry/index.js"

firebase.initializeApp(firebaseConfig)
ReactDOM.render(
    <HashRouter>
      <Switch>
        <Route path="/" component={Admin} />
        <Redirect from="*" to="/" />
      </Switch>
    </HashRouter>,
  document.getElementById("root")
);
