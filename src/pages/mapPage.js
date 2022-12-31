import { useState, useRef, useEffect } from "react"
import { MapCanvas } from "../components/mapCanvas"
import { ToolsSection } from "../components/toolsSection"
import { useSearchParams } from "react-router-dom"
import { PageTitle } from "../components/pageTitle"
import { Button } from "../components/Button"
import Swal from "sweetalert2"

export const MapPage = () => {
  const [params,] = useSearchParams()
  const linkRef = useRef(null)
  const [map,setMap] = useState({width: 100, height: 100, items: []})
  const colContainerRef = useRef(null)
  const [creating,setCreating] = useState(null)
  useEffect(()=>{
    setMap(map=>({
      ...map,
      width: params.get('w') || 100,
      height: params.get('h') || 100
    }))
  },[params])
  return (
    <div className='fixed inset-x-2 overflow-hidden top-16 bottom-2 grid-cols-5 grid gap-5'>
      <PageTitle title={'Add Map'}/>
      <div className="col-span-4 bg-[#232639] relative rounded-md">
        <div className="absolute inset-5 flex" ref={colContainerRef}>
          <MapCanvas handleChangeMap={setMap} map={map} creating={creating} handleUncreate={()=>setCreating(null)} containerRef={colContainerRef}/>
        </div>
        <Button onClick={async()=>{
          try{
            if(!map.name){
              await Swal.fire('Error','Please enter a name for the map','error')
              return
            }
            const json = JSON.stringify(map);
            const blob = new Blob([json], { type: 'application/json' });
            const url = URL.createObjectURL(blob);
            linkRef.current.download = `${map.name}.json`;
            linkRef.current.href = url;
            linkRef.current.click();
          }catch(e){
            console.error(e)
          }
        }} icon={'bi bi-file-earmark-arrow-down-fill'} className="bg-sky-400 text-white absolute z-[990] top-6 right-6 rounded-md aspect-square text-2xl hover:after:content-['Download'] hover:after:ml-2 hover:aspect-auto after:text-base"/>
      </div>
      <a ref={linkRef} style={{ display: 'none' }}>download</a>
      <div className="col-span-1">
        <ToolsSection creating={creating} setCreating={setCreating} map={map} setMap={setMap}/>
      </div>
    </div>
  )
}