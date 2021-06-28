import React from "react";
import DatasetsTable from "components/Datasets/DatasetsTable";

export default function DatasetsView() {
  return (
    <>
      <div className="flex flex-wrap mh-full">
        <div className="w-full mb-12 px-4">
		      <DatasetsTable />
        </div>
      </div>
    </>
  );
}
