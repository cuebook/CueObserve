import React, { createContext, useState } from 'react';

// this is the equivalent to the createStore method of Redux
// https://redux.js.org/api/createstore

// const [databases, setDatabases] = useState([])
let searchCardData = {}
const updateSearchCardData = x => searchCardData = x

export const GlobalContext = createContext();

export const GlobalContextProvider = ({ children }) => {
	return (
		<GlobalContext.Provider value={{searchCardData, updateSearchCardData}} >
			{children}
		</GlobalContext.Provider>
		)
}

// export default { GlobalContext, GlobalContextProvider };