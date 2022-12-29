import { useState, useRef } from "react"
import { MapCanvas } from "../components/mapCanvas"
import { ToolsSection } from "../components/toolsSection"

export const MapPage = () => {
  const [map,setMap] = useState({width: 84, height: 50, items: []})
  const colContainerRef = useRef(null)
  const [creating,setCreating] = useState(null)
  return (
    <div className='fixed inset-x-2 overflow-hidden top-8 bottom-2 grid-cols-5 grid gap-5'>
      <div className="col-span-4 bg-[#232639] relative rounded-md">
        <div className="absolute inset-5 flex" ref={colContainerRef}>
          <MapCanvas handleChangeMap={setMap} map={map} creating={creating} handleUncreate={()=>setCreating(null)} containerRef={colContainerRef}/>
        </div>
      </div>
      <div className="col-span-1">
        <ToolsSection creating={creating} setCreating={setCreating}/>
      </div>
    </div>
  )
}