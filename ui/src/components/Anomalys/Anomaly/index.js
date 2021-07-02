import React, { useState, useEffect, useRef } from "react";
import style from "./style.module.scss";
import { useParams, useHistory } from 'react-router-dom';
import { message } from "antd"
import _ from "lodash";
import { Chart, Geom, Axis, Tooltip, track, G2, View } from "bizcharts";
track(false);
G2.track(false);

import anomalyService from "services/anomalys";

const { Option } = Select;

export default function Anomaly(props) {
  useEffect(() => {
    getDataset();
  }, []);

  const chart = (
      <Chart scale={cols} forceFit={true} height={400}
        onClick={e => this.handleChartClick(e)}
      >
        <Tooltip crosshairs={{ type: "line" }} />
        <View data={data.band}>
          <Axis name="ts" />
          <Axis name="val" />
          <Geom
            type="area"
            position="ts*val"
            tooltip={false}
            style={{ fillOpacity: 0.15 }}
            color={"#999"}
          />
        </View>
        <View data={data.values}>
          <Geom
            type="point"
            position="ts*val"
            size={"anomaly"}
            opacity={['anomaly', (anomaly)=>{
              if(anomaly == 1)
                return 0;
              return 0.5;
            }]}
            color="#ff1100"
            shape="circle"
            tooltip={false}
            style={{ stroke: "#fff", lineWidth: 1, fillOpacity: 0.5 }}
          />
          <Geom type="line" position="ts*val" size={2} />
        </View>
      </Chart>
    );


  return (<>
      <p>Insert card here</p>
  </>)

}
