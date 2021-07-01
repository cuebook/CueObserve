import React from "react";
import Anomaly from "components/Anomalys/Anomaly";

export default function AnomalyView() {
  return (
    <>
      <div className="flex flex-wrap mh-full">
        <div className="w-full mb-12 px-4">
		      <Anomaly />
        </div>
      </div>
    </>
  );
}
