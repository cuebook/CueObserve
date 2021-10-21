import React from "react";
import SearchResultPage from "components/Search/SearchResult/SearchResultPage"

export default function SearchResultsView() {
  return (
    <>
      <div className="flex flex-wrap mh-full">
        <div className="w-full mb-12 px-4">
		      <SearchResultPage />
        </div>
      </div>
    </>
  );
}
