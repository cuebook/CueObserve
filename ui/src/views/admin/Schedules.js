import React from "react";
import Schedule from "components/Schedules/Schedule.js"


export default function SchedulesView() {
  return (
    <>
      <div className="flex flex-wrap mh-full">
        <div className="w-full mb-12 px-4">
		      <Schedule />
        </div>
      </div>
    </>
  );
}
