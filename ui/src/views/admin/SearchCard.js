import React from "react";
import SearchCardPage from "components/Search/Card/CardPage"

export default function SearchCardPageView() {
  return (
    <>
      <div className="flex flex-wrap mh-full">
        <div className="w-full mb-12 px-4">
		      <SearchCardPage />
        </div>
      </div>
    </>
  );
}
