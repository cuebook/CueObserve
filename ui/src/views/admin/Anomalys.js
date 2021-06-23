import React from "react";
import AnomalyTable from "components/Anomalys/AnomalyTable.js";


export default function AnomalyTableFunction() {
  return (
    <>
      <div className="flex flex-wrap mh-full">
        <div className="w-full mb-12 px-4">
		      <AnomalyTable />
        </div>
      </div>
    </>
  );
}
