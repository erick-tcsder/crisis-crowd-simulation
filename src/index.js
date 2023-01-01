import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';
import {createBrowserRouter,RouterProvider, Link} from 'react-router-dom'
import { MapPage } from './pages/mapPage';
import { SetupPage } from './pages/setupPage';
import { SimulationPage } from './pages/simulationPage';
import { PageTitle } from './components/pageTitle';


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
        path: '/vulnerability',
        element: <PageTitle title={'Vulnerability Test'}/>
      },
      {
        index: true,
        element: <SetupPage/>
      }
    ],
    errorElement: <div className='fixed inset-5 flex'>
      <div className='flex flex-col m-auto'>
        <span className='text-8xl font-bold text-sky-400 '>404</span>
        <span className='uppercase text-xs tracking-tight text-white text-opacity-60'>Opps ... this is not the page you are looking for (I supose)</span>
        <Link className='' to={'/'}>Home</Link>
      </div>
      <div className='blur-3xl bg-sky-400 opacity-25 aspect-square w-80 rounded-full fixed left-1/2 top-1/2'/>
    </div>
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
