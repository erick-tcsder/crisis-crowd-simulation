import { useStreamingVuln } from "../hooks/simulationStream"
import {useRef,useEffect,useCallback,useState} from 'react'
import { useSearchParams } from "react-router-dom"
import { SimulationService } from "../hooks/simulationservice"
import {PageTitle} from '../components/pageTitle'


export const VulnerabilityPage = ()=>{
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
  const {events} = useStreamingVuln(loading,maps,{
    bombRadius: parseFloat(params.get('br')),
    peopleCount: parseInt(params.get('pc'))
  },(newState)=>{
    const li = document.createElement('li')
    li.innerText = JSON.stringify(newState)
    ulRef.current.appendChild(li)
  })
  return (
    <div className='fixed inset-x-3 top-16 bottom-3 grid-cols-4 grid gap-9 overflow-auto p-5'>
      <PageTitle title={'Vulnerability Test'}/>
      <ul ref={ulRef}/>
    </div>
  )
}