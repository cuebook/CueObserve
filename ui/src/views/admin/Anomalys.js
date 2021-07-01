import React from "react";
import AnomalysTable from "components/Anomalys/AnomalysTable";

export default function AnomalysView() {
  return (
    <>
      <div className="flex flex-wrap mh-full">
        <div className="w-full mb-12 px-4">
		      <AnomalysTable />
        </div>
      </div>
    </>
  );
}
