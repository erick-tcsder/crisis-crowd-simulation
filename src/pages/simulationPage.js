import { useRef, useState,useCallback, useEffect} from "react"
import { PageTitle } from "../components/pageTitle"
import { useStreamingAssets } from "../hooks/simulationStream"
import { SimulationService } from "../hooks/simulationservice"
import { useSearchParams } from 'react-router-dom'

export const SimulationPage = ()=>{
  const ulRef = useRef(null)
  const [params,] = useSearchParams()
  const [maps,setMaps] = useState([])
  const [loading,setLoading] = useState(false)
  const getMaps = useCallback(()=>{
    setLoading(true)
    SimulationService.getMaps().then(maps=>setMaps(maps.data)).finally(()=>setLoading(false))
  },[])
  useEffect(()=>{
    getMaps()
  },[getMaps])
  const {positions} = useStreamingAssets(loading,maps,{
    mapBomb: params.get('mb'),
    bombTop: parseFloat(params.get('bt')),
    bombLeft: parseFloat(params.get('bl')),
    bombRadius: parseFloat(params.get('br')),
    peopleCount: parseInt(params.get('pc'))
  },(newState)=>{
    const li = document.createElement('li')
    li.innerText = JSON.stringify(newState)
    ulRef.current.appendChild(li)
  })
  return (
    <div className='fixed inset-x-3 top-16 bottom-3 grid-cols-4 grid gap-9 overflow-auto p-5'>
      <PageTitle title={'Simulation Started'}/>
      <ul ref={ulRef}/>
    </div>
  )
}