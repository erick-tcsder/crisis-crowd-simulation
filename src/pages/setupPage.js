import { useEffect, useState, useRef, useCallback } from "react"
import { SimulationService } from "../hooks/simulationservice"
import { MapCanvas } from "../components/mapCanvas"
import { Button } from "../components/Button"
import classNames from "classnames"
import Swal from "sweetalert2"
import {useNavigate} from 'react-router-dom'
import { PageTitle } from "../components/pageTitle"
import DragAndDropOverlay from "../components/draganddropoverlay"


const MapPrev = (props) => {
  const ref = useRef(null)
  const handleDelete = useCallback(()=>{
    SimulationService.deleteMap(props.m.name).then(props.getMaps)
  },[props.getMaps, props.m.name])
  return <div onClick={props.onClick} className={`col-span-1 self-start p-3 flex flex-col bg-[#232639] rounded-lg ${props.mapBomb === props.m.name ? 'ring-red-400 ring-4' : 'ring-sky-400 ring-2'} ring-opacity-50`}>
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
  const [mapBomb, setMapBomb] = useState('')
  const [maps,setMaps] = useState([])
  const getMaps = useCallback(()=>{
    SimulationService.getMaps().then(maps=>setMaps(maps.data))
  },[])
  useEffect(()=>{
    getMaps()
  },[getMaps])

  useEffect(()=>{
    setMapBomb(maps?.[0]?.name)
  },[maps])

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

  const handleStartSimulation = useCallback(async()=>{
    const {value: peopleCount} = await Swal.fire({
      title: 'People Count',
      input: 'number',
      inputLabel: 'People Count',
      inputPlaceholder: 'Enter the number of people on the building',
      inputAttributes: {
        min: 1,
        max: 300
      },
      confirmButtonText: 'Next',
      allowOutsideClick: false,
      allowEscapeKey: false,
      showCancelButton: true,
      cancelButtonText: 'Cancel',
    })
    const {value: bombTop} = await Swal.fire({
      title: 'Bomb Top',
      input: 'number',
      inputLabel: 'Bomb Top',
      inputPlaceholder: 'Enter the top coordinate of the bomb epicenter',
      confirmButtonText: 'Next',
      allowOutsideClick: false,
      allowEscapeKey: false,
      showCancelButton: true,
      cancelButtonText: 'Cancel'
    })
    const {value: bombLeft} = await Swal.fire({
      title: 'Bomb Left',
      input: 'number',
      inputLabel: 'Bomb Left',
      inputPlaceholder: 'Enter the left coordinate of the bomb epicenter',
      confirmButtonText: 'Next',
      allowOutsideClick: false,
      allowEscapeKey: false,
      showCancelButton: true,
      cancelButtonText: 'Cancel'
    })
    const {value: bombRadius} = await Swal.fire({
      title: 'Bomb Radius',
      input: 'number',
      inputLabel: 'Bomb Radius',
      inputPlaceholder: 'Enter the radius of the bomb',
      confirmButtonText: 'Next',
      allowOutsideClick: false,
      allowEscapeKey: false,
      showCancelButton: true,
      cancelButtonText: 'Cancel'
    })
    if(!peopleCount || !bombTop || !bombLeft || !bombRadius){
      return
    }
    await SimulationService.startSimulation(peopleCount,bombRadius,mapBomb,bombTop,bombLeft)
    navigator(`/simulation?pc=${peopleCount}&br=${bombRadius}&mb=${mapBomb}&bt=${bombTop}&bl=${bombLeft}`)
  },[mapBomb, navigator])
  
  const handleStartVulnerabilityAnasisys = useCallback(async()=>{
    const {value: peopleCount} = await Swal.fire({
      title: 'People Count',
      input: 'number',
      inputLabel: 'People Count',
      inputPlaceholder: 'Enter the number of people on the building',
      inputAttributes: {
        min: 1,
        max: 300
      },
      confirmButtonText: 'Next',
      allowOutsideClick: false,
      allowEscapeKey: false,
      showCancelButton: true,
      cancelButtonText: 'Cancel',
    })
    const {value: bombRadius} = await Swal.fire({
      title: 'Bomb Radius',
      input: 'number',
      inputLabel: 'Bomb Radius',
      inputPlaceholder: 'Enter the radius of the bomb',
      confirmButtonText: 'Next',
      allowOutsideClick: false,
      allowEscapeKey: false,
      showCancelButton: true,
      cancelButtonText: 'Cancel'
    })
    if(!peopleCount || !bombRadius){
      return
    }
    await SimulationService.startVulnerabilities(peopleCount,bombRadius)
    navigator(`/vulnerability?pc=${peopleCount}&br=${bombRadius}`)
  },[navigator])
  return (
    <>
      <PageTitle title={'Set up the Simulation'}/>

      <Button onClick={handleStartSimulation} icon={'bi bi-play-fill'} className="bg-sky-400 text-white fixed z-[990] bottom-36 right-6 rounded-full aspect-square text-3xl hover:after:content-['Start'] hover:aspect-auto after:text-base"/>
      <Button onClick={handleStartVulnerabilityAnasisys} icon={'fa-solid fa-skull'} className="bg-red-400 text-white fixed z-[990] bottom-20 right-6 rounded-full aspect-square text-3xl hover:after:content-['Vulnerabilities'] hover:after:ml-4 hover:aspect-auto after:text-base"/>

      <div className='fixed inset-x-3 top-16 bottom-3 grid-cols-4 grid gap-9 overflow-auto p-5'>
        {maps.map(m=> <MapPrev mapBomb={mapBomb} onClick={()=>setMapBomb(m.name)} m={m} key={m.name} getMaps={getMaps}/>)}
        {maps.length === 0 ? (<button onClick={handleAddMap}  className="col-span-1 p-3 group grid bg-[#232639] rounded-lg border-2 hover:border-solid hover:border-4 hover:border-opacity-100 border-sky-400 border-dashed border-opacity-50">
          <span className="place-self-center group-hover:text-sky-400 text-lg">+ Add Map <br/> Or drag & drop it</span>
        </button>) : <></>}
      </div>
      {maps.length === 0 ? (
        <DragAndDropOverlay/>
      ) : <></>}
    </>
  )
}