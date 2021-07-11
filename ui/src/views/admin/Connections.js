import React from "react";
import Connections from "components/Connections/index.js"


export default function ConnectionView() {
  return (
    <>
      <div className="flex flex-wrap mh-full">
        <div className="w-full mb-12 px-4">
		      <Connections />
        </div>
      </div>
    </>
  );
}
