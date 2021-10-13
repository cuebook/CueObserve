import React from "react";
import GlobalDimensionTable from "components/Search/GlobalDimension/index.js"

export default function DatasetsView() {
  return (
    <>
      <div className="flex flex-wrap mh-full">
        <div className="w-full mb-12 px-4">
		      <GlobalDimensionTable />
        </div>
      </div>
    </>
  );
}
