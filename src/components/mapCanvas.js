import { useEffect, useMemo, useRef, useState } from "react";
import { EnviromentFactory, envMapper } from "./enviromentFactory";
import { Utils } from "../utils";
import Swal from "sweetalert2";

export const getNewObstacle = async (coords,creating,map,canvas) => {
  const {start,end} = coords
  const x = Utils.getPxToM(map,canvas,Math.min(start.x,end.x))
  const y = Utils.getPxToM(map,canvas,Math.min(start.y,end.y)) 
  const w = Utils.getPxToM(map,canvas,start.x < end.x ? end.x - start.x : start.x - end.x)
  const h = Utils.getPxToM(map,canvas,start.y < end.y ? end.y - start.y : start.y - end.y)
  const min = Math.min(w,h)
  switch (creating) {
    case 'VWALL':
      return {
        OBJECT_TYPE: 'V_WALL',
        props:{
          top: y,
          left: x, 
          height: h
        }
      }
    case 'HWALL':
      return {
        OBJECT_TYPE: 'H_WALL',
        props:{
          top: y,
          left: x, 
          width: w
        }
      }
    case 'RECT':
      return {
        OBJECT_TYPE: 'RECTANGULAR_OBJ',
        props:{
          top: y,
          left: x, 
          width: w,
          height: h
        }
      }
    case 'CIRC':
      return {
        OBJECT_TYPE: 'CIRCULAR_OBJ',
        props:{
          top: y,
          left: x, 
          width: min,
          height: min,
          radius: min
        }
      }
    case 'UP':
    case 'RIGHT':
    case 'DOWN':
    case 'LEFT':
      return {
        OBJECT_TYPE: 'EVAC_SIGN',
        props:{
          top: y,
          left: x, 
          width: w,
          height: h,
          direction: creating.toLowerCase() 
        }
      }
    case 'DOOR':
      return {
        OBJECT_TYPE: 'DOOR',
        props:{
          top: y,
          left: x, 
          width: w,
          height: h
        }
      }
    case 'EXIT':
      return {
        OBJECT_TYPE: 'EVAC_EXIT',
        props:{
          top: y,
          left: x, 
          width: w,
          height: h
        }
      }
    case 'SAFE':
      return {
        OBJECT_TYPE: 'SAFE_ZONE',
        props:{
          top: y,
          left: x, 
          width: w,
          height: h
        }
      }
    case 'STAIRS':
      const { value: label } = await Swal.fire({
        title: 'Stair Name',
        input: 'text',
        inputLabel: 'Name',
        inputValue: "A",
        showCancelButton: true,
        inputValidator: (value) => {
          if (!value) {
            return 'You need to write something!'
          }
        }
      })
      return {
        OBJECT_TYPE: 'STAIRS',
        props:{
          top: y,
          left: x, 
          width: w,
          height: h,
          label:label
        }
      }
    case 'ELEVATOR':
      const { value: labelEl } = await Swal.fire({
        title: 'Elevator Name',
        input: 'text',
        inputLabel: 'Name',
        inputValue: "A",
        showCancelButton: true,
        inputValidator: (value) => {
          if (!value) {
            return 'You need to write something!'
          }
        }
      })
      return {
        OBJECT_TYPE: 'ELEVATOR',
        props:{
          top: y,
          left: x, 
          width: w,
          height: h,
          label: labelEl
        }
      }
    case 'DAMAGE_ZONE':
      return {
        OBJECT_TYPE: 'DAMAGE_ZONE',
        props:{
          top: y,
          left: x, 
          width: w,
          height: h,
          damageFactor: 0.1
        }
      }
    default:
      return {}
  }
}

export const MapCanvas = ({ map, handleChangeMap, creating, handleUncreate, ...props }) => {
  const canvasRef = useRef(null);
  const creatingShape = useRef(null);
  const creatingCanvas = useRef(null);
  const [dims,setDims] = useState(null)
  const crtng = useRef(false)
  const crshape = useRef(null)
  const coordsRef = useRef({})
  const aspectRatio = useMemo(() => {
    return map.width / map.height;
  }, [map]);

  useEffect(()=>{
    crshape.current = creating
  },[creating])

  useEffect(()=>{
    const canv = creatingCanvas.current
    if(canv && creatingShape.current){
      canv.className = 'absolute inset-0 bg-transparent z-[99]'
      creatingShape.current.className = 'hidden z-[98]'
    }
    const el1 = (e)=>{
      const bb = canv.getBoundingClientRect()
      coordsRef.current = {
        start: {
          x: e.clientX - bb.left,
          y: e.clientY - bb.top
        }
      }
    }
    canv.addEventListener('mousedown', el1)

    const el2 = (e)=>{
      const bb = canv.getBoundingClientRect()
      if(!coordsRef.current.start) {
        creatingShape.current.style.display = 'none'
      }
      if(coordsRef.current.start){
        coordsRef.current = {
          ...coordsRef.current,
          end: {
            x: e.clientX - bb.left,
            y: e.clientY - bb.top
          }
        }
        const {start, end} = coordsRef.current
        const x = Math.min(start.x,end.x)
        const y = Math.min(start.y,end.y)
        const w = start.x < end.x ? end.x - start.x : start.x - end.x
        const h = start.y < end.y ? end.y - start.y : start.y - end.y
        const min = Math.min(w,h)
        if([].includes(crshape.current)){
          creatingShape.current.style.width = `${min}px`
          creatingShape.current.style.height = `${min}px`
        }else if ([].includes(crshape.current)){
          creatingShape.current.style.width = `${w}px`
          creatingShape.current.style.height = `${h}px`
        }else{
          creatingShape.current.style.width = `${w}px`
          creatingShape.current.style.height = `${h}px`
        }
        creatingShape.current.style.left = `${x}px`
        creatingShape.current.style.top = `${y}px`
        creatingShape.current.style.display = 'block'
      }
    }
    canv.addEventListener('mousemove', el2)

    const el3 = async(e)=>{
      if(crtng.current || !crtng || !coordsRef.current.start) return
      crtng.current = true
      const bb = canv.getBoundingClientRect()
      coordsRef.current = {
        ...coordsRef.current,
        end: {
          x: e.clientX < bb.left ? 0 : e.clientX > bb.left + bb.width ? bb.width : e.clientX - bb.left,
          y: e.clientY < bb.top ? 0 : e.clientY > bb.top + bb.height ? bb.height : e.clientY - bb.top
        }
      }
      if(!coordsRef.current.start || !coordsRef.current.end) {
        crtng.current = false;
        return
      }
      const newNode = await getNewObstacle(coordsRef.current,crshape.current,map,{width: bb.width, height: bb.height})
      if(newNode){
        handleChangeMap((map)=>({
          ...map,
          items: [...map.items, newNode]
        }))
      }
      coordsRef.current = {}
      crtng.current = false
    }
    window.addEventListener('mouseup', el3)
    const el4 = (e)=>{
      if(e.key === 'z' && e.ctrlKey){
        handleChangeMap((map)=>({
          ...map,
          items: map.items.slice(0,-1)
        }))
      }
    }
    window.addEventListener('keydown', el4)
    return ()=>{
      canv.removeEventListener('mousedown', el1)
      canv.removeEventListener('mousemove', el2)
      window.removeEventListener('mouseup', el3)
      window.removeEventListener('keydown', el4)
    }
  },[])

  useEffect(() => {
    if (creating) {
      creatingCanvas.current.className = 'absolute inset-0 bg-transparent z-[99]'
      creatingShape.current.className = 'absolute bg-sky-500 bg-opacity-20 border-sky-600 border'
    } else {
      creatingCanvas.current.className = 'hidden'
      creatingShape.current.className = 'hidden'
    }
  },[creating])

  useEffect(()=>{
    const {height: h, width: w} = props.containerRef?.current?.getBoundingClientRect()
    const th = h*aspectRatio > w ? w/aspectRatio : h
    const tw = h*aspectRatio > w ? w : h*aspectRatio
    setDims({
      width: tw,
      height: th
    })
    canvasRef.current.style.width=`${tw}px`;
    canvasRef.current.style.height=`${th}px`;
    canvasRef.current.style.display = 'flex'
  },[aspectRatio, props.containerRef, setDims])
  return (
    <div ref={canvasRef} className='m-auto bg-white relative'>
      {map.items.map((obj,index) => (
        <EnviromentFactory
          canvas={dims}
          map={map}
          envOjb={obj}
          enviromentMapper={envMapper}
          key={index}
        />
      ))}
      <div ref={creatingShape}/>
      <div className="" ref={creatingCanvas}></div>
    </div>
  );
};
