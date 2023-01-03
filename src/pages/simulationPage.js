import { useRef, useState,useCallback, useEffect, useMemo} from "react"
import { PageTitle } from "../components/pageTitle"
import { useStreamingAssets } from "../hooks/simulationStream"
import { SimulationService } from "../hooks/simulationservice"
import { useSearchParams } from 'react-router-dom'
import { MapCanvas } from "../components/mapCanvas"
import Swal from "sweetalert2"

export const SimulationPage = ()=>{
  const containerRef = useRef(null)
  const [params,] = useSearchParams()
  const [maps,setMaps] = useState([])
  const [loading,setLoading] = useState(false)
  const [positions,setPositions] = useState([])
  const [time,setTime] = useState(0)
  const sProps = useMemo(()=>{
    return {
      mapBomb: params.get('mb'),
      bombTop: parseFloat(params.get('bt')),
      bombLeft: parseFloat(params.get('bl')),
      bombRadius: parseFloat(params.get('br')),
      peopleCount: parseInt(params.get('pc'))
    }
  },[])
  const getMaps = useCallback(()=>{
    setLoading(true)
    SimulationService.getMaps().then(maps=>setMaps(maps.data)).finally(()=>setLoading(false))
  },[])
  const onSchange = useCallback((newState)=>{
    console.log('asd')
    setPositions(newState.ped)
    setTime(newState.time)
  },[])
  const onSEnd = useCallback(()=>{
    Swal.fire('Simulation Ende','The simulation has ended','info')
  },[]) 
  useEffect(()=>{
    getMaps()
  },[getMaps])
  useStreamingAssets(loading,maps,sProps,onSchange,onSEnd)
  return (
    <div className='fixed inset-x-3 top-16 bottom-3 grid-cols-4 grid gap-9 overflow-auto p-5'>
      <PageTitle title={`Simulation Started ${time}`}/>
      <div className="absolute inset-5 flex" ref={containerRef}>
        <MapCanvas handleChangeMap={()=>{}} havePedestrians={true} pedestrianPositions={positions} map={maps?.[0]} creating={null} handleUncreate={()=>{}} containerRef={containerRef}/>
      </div>
    </div>
  )
}