import React, { useState, useEffect, useRef } from "react";
import style from "./style.module.scss";
import { useParams, useHistory } from 'react-router-dom';
import { Chart, Geom, Axis, Tooltip, View, Legend } from "bizcharts";

export default function AnomalyChart(props) {
  const anomalyData = props.data;

  const calculateMin =  actualData => {
    let min = actualData.length > 0 ? actualData[0].val : 0;
      for (let i = 0; i < actualData.length; i++) {
        if (actualData[i].val < min) {
          min = actualData[i].val;
        }
      }
    return min
  }

  if (!anomalyData) return null;

  const min = calculateMin(anomalyData.data.anomalyData.actual)

  // find min & null vals
  var deno = 1,
    postfix = "";
  if (min > 1000000000) {
    deno = 1000000000;
    postfix = "B";
  } else if (min > 1000000) {
    deno = 1000000;
    postfix = "M";
  } else if (min > 1000) {
    deno = 1000;
    postfix = "K";
  }

  const cols = {
    y: {
      alias: anomalyData.metric
        ? anomalyData.metric
        : "Value",
      sync: true,
      formatter: y => {
        return (y / deno).toString() + postfix;
      }
    },
    ds: {
      sync: true,
      type: "time",
      alias: anomalyData.timestampAlias
        ? anomalyData.timestampAlias
        : "Time",
      mask: anomalyData.granularity == "day" ? "YYYY-MM-DD" : "YYYY-MM-DD HH:00"
    }
  };

  const bandView = anomalyData.data.anomalyData.band ? (<View data={anomalyData.data.anomalyData.band}>
          <Geom
            type="area"
            position="ds*y"
            tooltip={false}
            style={{ fillOpacity: 0.15 }}
            color={"#777"}
          />
        </View>) : null
  
  const predictedView = anomalyData.data.anomalyData.predicted ? (<View data={anomalyData.data.anomalyData.predicted}>
    <Geom
      type="line"
      position={"ds*y"}
      size={2}
      style={{ lineDash: [4, 4] }}
    />
  </View>) : null


  const chart = (
    <div className={style.chartDiv}>
      <Chart scale={cols} autoFit padding={ props.isMiniChart ? [5, 5, 5, 5] : [10, 10, 25, 20]} height={ props.isMiniChart ? 80 : 400 }>
        { props.isMiniChart ? 
          <>
            <Axis name="ds" visible={false} />
            <Axis name="y" grid={null} line={null} visible={false} />
          </>
          :
          <>
            <Axis name="ds" />
            <Axis name="y" />
          </>
        }
        <Legend visible={false} />
        <Tooltip crosshairs={{ type: "line" }} />
          {bandView}
          <View data={anomalyData.data.anomalyData.actual}>
            <Geom
              type="point"
              position="ds*y"
              size={[
                "anomaly",
                anomaly => {
                  if (anomaly === 1) return 0;
                  return anomaly;
                }
              ]}
              opacity={[
                "anomaly",
                anomaly => {
                  if (anomaly === 1) return 0;
                  return 0.5;
                }
              ]}
              color= "#ff1100"
              shape="circle"
              tooltip={false}
              style={{ stroke: "#fff", lineWidth: 1, fillOpacity: 0.5 }}
              select={[
                true,
                {
                  mode: "single",
                  style: {
                    fill: "black",
                    opacity: "0.3"
                  },
                  cancelable: true,
                  animate: true
                }
              ]}
              active={[
                true,
                {
                  highlight: true,
                  style: {
                    cursor: "crosshair"
                  }
                }
              ]}
              active={[
                true,
                {
                  highlight: true,
                  style: {
                    cursor: "crosshair"
                  }
                }
              ]}
            />
            <Geom
              type="line"
              position={"ds*y"}
              size={props.isMiniChart ? 1.4 : 2}
            />
          </View>
          {predictedView}
        </Chart>
      </div>

    )

  return (<> { chart } </>)
}
