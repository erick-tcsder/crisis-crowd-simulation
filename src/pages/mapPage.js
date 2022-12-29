import { useState, useRef, useEffect } from "react"
import { MapCanvas } from "../components/mapCanvas"
import { ToolsSection } from "../components/toolsSection"
import { useSearchParams } from "react-router-dom"

export const MapPage = () => {
  const [params,setParams] = useSearchParams()
  const [map,setMap] = useState({width: 100, height: 100, items: []})
  const colContainerRef = useRef(null)
  const [creating,setCreating] = useState(null)
  useEffect(()=>{
    setMap(map=>({
      ...map,
      width: params.get('w') || 100,
      height: params.get('h') || 100
    }))
  },[])
  return (
    <div className='fixed inset-x-2 overflow-hidden top-8 bottom-2 grid-cols-5 grid gap-5'>
      <div className="col-span-4 bg-[#232639] relative rounded-md">
        <div className="absolute inset-5 flex" ref={colContainerRef}>
          <MapCanvas handleChangeMap={setMap} map={map} creating={creating} handleUncreate={()=>setCreating(null)} containerRef={colContainerRef}/>
        </div>
      </div>
      <div className="col-span-1">
        <ToolsSection creating={creating} setCreating={setCreating} map={map} setMap={setMap}/>
      </div>
    </div>
  )
}