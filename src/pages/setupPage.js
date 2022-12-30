import { useEffect, useState, useRef } from "react"
import { SimulationService } from "../hooks/simulationservice"
import { MapCanvas } from "../components/mapCanvas"


const MapPrev = (props) => {
  const ref = useRef(null)
  return <div className="h-[500px] w-[500px]" ref={ref}>
    <MapCanvas containerRef={ref} map={props.m} key={props.m.name} creating={null} handleChangeMap={()=>{}}/>
  </div>
}

export const SetupPage = (props)=>{
  const [maps,setMaps] = useState([])
  useEffect(()=>{
    SimulationService.getMaps().then(maps=>setMaps(maps.data))
  },[])

  return (
    <div className='fixed inset-x-2 overflow-hidden top-8 bottom-2 grid-cols-5 grid gap-5'>
      {maps.map(m=> <MapPrev m={m} key={m.name}/>)}
    </div>
  )
}