import React from 'react';
import logo from './logo.svg';
import './App.scss';
import {
  BrowserRouter,
  Routes,
  Route
} from "react-router-dom";
import routes from "./routeConfig"
import AppRouter from './appRouter';
import history from "./history.js"
import {UserContextProvider} from "./Components/ContextProvider"

function App() {
  return (
    <UserContextProvider>
      <BrowserRouter history={history}>
        <Routes>
          {routes.map((route, index) => {
            const Component = route.component
            return (<Route
                      key={index}
                      path={route.path}
                      element={
                        <AppRouter isPrivate={route.isPrivate}>
                          <Component/>
                        </AppRouter>
              }
            />)
          }
          )}
        </Routes>
      </BrowserRouter>
    </UserContextProvider>
  );
}

export default App;
