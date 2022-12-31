import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';
import {createBrowserRouter,RouterProvider} from 'react-router-dom'
import { MapPage } from './pages/mapPage';
import { SetupPage } from './pages/setupPage';
import { SimulationPage } from './pages/simulationPage';


const router = createBrowserRouter([
  {
    path: '/',
    element: <App/>,
    children: [
      {
        path: '/map/new',
        element: <MapPage/>
      },
      {
        path: '/simulation',
        element: <SimulationPage/>
      },
      {
        index: true,
        element: <SetupPage/>
      }
    ],
    errorElement: <div>404</div>
  }
])

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
    <RouterProvider router={router}/>
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
// reportWebVitals(console.log);
