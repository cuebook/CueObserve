import React, { useState, useEffect, useRef } from "react";
import style from "./style.module.scss";
import { useParams, useHistory } from 'react-router-dom';
import anomalyService from "services/anomalys";
import AnomalyChart from "components/Anomalys/AnomalyChart"
import RootCauseAnalysis from "components/RootCauseAnalysis"

export default function Anomaly(props) {
  const [ anomalyData, setAnomalyData ] = useState(null);
  const params = useParams()

  useEffect(() => {
    getAnomaly();
  }, []);


  const getAnomaly = async () => {
    const data = await anomalyService.getAnomaly(params.anomalyId)
    if (data) {
      setAnomalyData(data);
    }
  }

  if (!anomalyData) return null;

  return (<>
    <div className="flex">
    <div className={`w-10/12 ${style.chartPanel}`}>
      <div className={style.anomalyTitle} dangerouslySetInnerHTML={{ __html: anomalyData.title }} />
      <p />
      <div className={style.anomalyText} dangerouslySetInnerHTML={{ __html: anomalyData.text }} />
      <div className={style.chartDiv}> <AnomalyChart data={anomalyData} /> </div>
      < RootCauseAnalysis anomalyId={params.anomalyId} />
    </div>
    </div>
  </>)

}
