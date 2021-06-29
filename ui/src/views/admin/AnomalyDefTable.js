import React from "react";
import AnomalyTable from "components/AnomalyDefinition/AnomalyDefTable.js"


export default function ConnectionFunctions() {
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
