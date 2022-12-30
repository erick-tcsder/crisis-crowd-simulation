import { useEffect, useState, useRef, useCallback } from "react"
import { SimulationService } from "../hooks/simulationservice"
import { MapCanvas } from "../components/mapCanvas"
import { Button } from "../components/Button"
import classNames from "classnames"
import Swal from "sweetalert2"
import {useNavigate} from 'react-router-dom'
import { PageTitle } from "../components/pageTitle"


const MapPrev = (props) => {
  const ref = useRef(null)
  const handleDelete = useCallback(()=>{
    SimulationService.deleteMap(props.m.name).then(props.getMaps)
  },[props.getMaps, props.m.name])
  return <div className="col-span-1 self-start p-3 flex flex-col bg-[#232639] rounded-lg ring-2 ring-sky-400 ring-opacity-50">
    <div className="aspect-square w-full grid place-content-center bg-[#232639]" ref={ref}>
      <MapCanvas containerRef={ref} map={props.m} key={props.m.name} creating={null} handleChangeMap={()=>{}}/>
    </div>
    <span className="text-xl font-bold">{props.m.name}</span>
    <span className="my-3 text-sm tracking-wide text-opacity-50 ">{props.m?.width}x{props.m?.height}</span>
    <div>
      <Button onClick={handleDelete} icon={'bi bi-x-lg'} className={classNames({
        'rounded-md px-3 py-2 my-auto':true,
        'ring-2 ring-red-500 text-red-500 hover:bg-red-400 hover:bg-opacity-30 ring-inset': true
      })}>Remove</Button>
    </div>
  </div>
}

export const SetupPage = (props)=>{
  const navigator = useNavigate()
  const [maps,setMaps] = useState([])
  const getMaps = useCallback(()=>{
    SimulationService.getMaps().then(maps=>setMaps(maps.data))
  },[])
  useEffect(()=>{
    getMaps()
  },[getMaps])

  const handleAddMap = useCallback(async()=>{
    const {value: w} = await Swal.fire({
      title: 'Map Width',
      input: 'number',
      inputLabel: 'Width',
      inputPlaceholder: 'Enter the width of the map',
      inputAttributes: {
        min: 1,
      },
      confirmButtonText: 'Next',
      allowOutsideClick: false,
      allowEscapeKey: false,
      showCancelButton: true,
      cancelButtonText: 'Cancel',
    })
    const {value: h} = await Swal.fire({
      title: 'Map Height',
      input: 'number',
      inputLabel: 'Height',
      inputPlaceholder: 'Enter the height of the map',
      inputAttributes: {
        min: 1,
      },
      confirmButtonText: 'Next',
      allowOutsideClick: false,
      allowEscapeKey: false,
      showCancelButton: true,
      cancelButtonText: 'Cancel'
    })
    if(!w || !h){
      return
    }
    navigator(`/map/new?w=${w}&h=${h}`)
  },[navigator])

  return (
    <>
      <PageTitle title={'Set up the Simulation'}/>
      <div className='fixed inset-x-3 top-16 bottom-3 grid-cols-4 grid gap-9 overflow-auto p-5'>
        {maps.map(m=> <MapPrev m={m} key={m.name} getMaps={getMaps}/>)}
        <button onClick={handleAddMap}  className="col-span-1 p-3 group grid bg-[#232639] rounded-lg border-2 hover:border-solid hover:border-4 hover:border-opacity-100 border-sky-400 border-dashed border-opacity-50">
          <span className="place-self-center group-hover:text-sky-400 text-lg">+ Add Map</span>
        </button>
      </div>
    </>
  )
}