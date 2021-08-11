import React from "react";
import Settings from "components/Settings"

export default function SettingsView() {
  return (
    <>
      <div className="flex flex-wrap mh-full">
        <div className="w-full mb-12 px-4">
		      <Settings />
        </div>
      </div>
    </>
  );
}
