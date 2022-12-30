import { Outlet, useNavigate } from "react-router-dom";
import {Button} from './components/Button'
import classNames from "classnames";
import { SimulationService } from "./hooks/simulationservice";

function App() {
  const navigator = useNavigate()
  return (
    <div className="fixed inset-0">
      <header className="flex p-3 flex-row justify-between absolute inset-x-0 top-0 h-16 z-[999] shadow-2xl border-b-2 border-sky-400 border-opacity-20">
        <div id='page-title-portal'/>
        <div id='page-actions-portal'/>
        <div className="flex flex-row gap-x-4">
          <Button onClick={async()=>{
            try{
              navigator('/')
            }catch(e){
              console.error(e)
            }
          }} className={classNames({
            'rounded-md px-3 py-2':true,
            'bg-sky-500 text-white hover:ring-sky-300 hover:ring-2 hover:ring-offset-2 hover:ring-offset-[#121425]':true,
          })}>Home</Button>
          <Button onClick={async()=>{
            try{
              await SimulationService.restartSimulation()
              navigator('/')
              navigator(0)
            }catch(e){
              console.error(e)
            }
          }} className={classNames({
            'rounded-md px-3 py-2':true,
            'bg-sky-500 text-white hover:ring-sky-300 hover:ring-2 hover:ring-offset-2 hover:ring-offset-[#121425]':true,
          })}>Reset Simulation</Button>
        </div>
      </header>
      <Button onClick={async()=>{
        try{
          await SimulationService.startSimulation()
          navigator('/simulation')
        }catch(e){
          console.error(e)
        }
      }} icon={'bi bi-play-fill'} className="bg-sky-400 text-white fixed z-[999] bottom-20 right-6 rounded-full aspect-square text-3xl hover:after:content-['Start'] hover:aspect-auto after:text-base"/>
      <Outlet/>
    </div>
  );
}

export default App;
