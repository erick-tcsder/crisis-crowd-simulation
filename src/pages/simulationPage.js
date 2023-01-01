import { useRef, useState,useCallback, useEffect} from "react"
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
  const getMaps = useCallback(()=>{
    setLoading(true)
    SimulationService.getMaps().then(maps=>setMaps(maps.data)).finally(()=>setLoading(false))
  },[])
  useEffect(()=>{
    getMaps()
  },[getMaps])
  const sa = useStreamingAssets(loading,maps,{
    mapBomb: params.get('mb'),
    bombTop: parseFloat(params.get('bt')),
    bombLeft: parseFloat(params.get('bl')),
    bombRadius: parseFloat(params.get('br')),
    peopleCount: parseInt(params.get('pc'))
  },(newState)=>{
    console.log(newState)
    // setPositions(newState)
  },()=>{
    Swal.fire('Simulation Ended','The simulation has ended','info')
  })
  return (
    <div className='fixed inset-x-3 top-16 bottom-3 grid-cols-4 grid gap-9 overflow-auto p-5'>
      <PageTitle title={'Simulation Started'}/>
      <div className="absolute inset-5 flex" ref={containerRef}>
        <MapCanvas handleChangeMap={()=>{}} havePedestrians={true} pedestrianPositions={positions} map={maps?.[0]} creating={null} handleUncreate={()=>{}} containerRef={containerRef}/>
      </div>
    </div>
  )
}