import React from "react";
import Dataset from "components/Datasets/Dataset";

export default function DatasetView() {
  return (
    <>
      <div className="flex flex-wrap mh-full">
        <div className="w-full mb-12 px-4">
		      <Dataset />
        </div>
      </div>
    </>
  );
}
