import { useEffect, useRef } from "react"
import classNames from "classnames"
import {Utils} from "../utils"



export const Pedestrian = ({ id,top, left, width, status='ALIVE',map,canvas})=>{
  const ref = useRef(null)
  useEffect(()=>{
    if(!ref.current || !top || !left || !width || !map || !canvas) return
    console.log(map,canvas,left,top)
    if(top > map.height || left > map.width) console.log('aqui')
    const maxWidth = Math.max(Utils.getMToPx(map,canvas,width),10)
    ref.current.style.top = `${Utils.getMToPx(map,canvas,top - (width/2))}px`
    ref.current.style.left = `${Utils.getMToPx(map,canvas,left - (width/2))}px` 
    ref.current.style.width = `${maxWidth}px`
    ref.current.style.height = `${maxWidth}px`
    console.log(id)
  },[canvas, id, left, map, top, width])
  
  return <div className={classNames("absolute rounded-full transition-all text-white",{
    "bg-sky-500": status === "ALIVE",
    "bg-red-500": status === "DEAD",
    "bg-lime-500": status === "SAFE"
  })} ref={ref}>
    {status === 'ALIVE' ? <svg className="inset-2 fill-white absolute" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 512"><path d="M224 256c70.7 0 128-57.3 128-128S294.7 0 224 0S96 57.3 96 128s57.3 128 128 128zm-45.7 48C79.8 304 0 383.8 0 482.3C0 498.7 13.3 512 29.7 512H418.3c16.4 0 29.7-13.3 29.7-29.7C448 383.8 368.2 304 269.7 304H178.3z"/></svg>
    : status === 'DEAD' ? <svg  className="inset-2 fill-white absolute"xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><path d="M416 398.9c58.5-41.1 96-104.1 96-174.9C512 100.3 397.4 0 256 0S0 100.3 0 224c0 70.7 37.5 133.8 96 174.9c0 .4 0 .7 0 1.1v64c0 26.5 21.5 48 48 48h48V464c0-8.8 7.2-16 16-16s16 7.2 16 16v48h64V464c0-8.8 7.2-16 16-16s16 7.2 16 16v48h48c26.5 0 48-21.5 48-48V400c0-.4 0-.7 0-1.1zM224 256c0 35.3-28.7 64-64 64s-64-28.7-64-64s28.7-64 64-64s64 28.7 64 64zm128 64c-35.3 0-64-28.7-64-64s28.7-64 64-64s64 28.7 64 64s-28.7 64-64 64z"/></svg>
    : <svg className="inset-2 fill-white absolute" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><path d="M256 0c4.6 0 9.2 1 13.4 2.9L457.7 82.8c22 9.3 38.4 31 38.3 57.2c-.5 99.2-41.3 280.7-213.7 363.2c-16.7 8-36.1 8-52.8 0C57.3 420.7 16.5 239.2 16 140c-.1-26.2 16.3-47.9 38.3-57.2L242.7 2.9C246.8 1 251.4 0 256 0z"/></svg>
  }
  <span className="absolute w-auto bg-white bg-opacity-10 text-sky-500 top-full p-1 rounded-sm uppercase">{id}</span>
  </div>
}

