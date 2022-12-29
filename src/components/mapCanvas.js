import { useEffect, useMemo, useRef, useState } from "react";
import { EnviromentFactory, envMapper } from "./enviromentFactory";

export const MapCanvas = ({ map, handleChangeMap, creating, handleUncreate, ...props }) => {
  const canvasRef = useRef(null);
  const creatingShape = useRef(null);
  const creatingCanvas = useRef(null);
  const [dims,setDims] = useState(null)
  const aspectRatio = useMemo(() => {
    return map.width / map.height;
  }, [map]);

  useEffect(()=>{
    if(creatingCanvas.current && creatingShape.current){
      creatingCanvas.current.className = 'absolute inset-0 bg-transparent z-[99]'
      creatingShape.current.className = 'hidden z-[98]'
    }
    creatingCanvas.current.addEventListener('', (e)=>{})
  },[])

  useEffect(() => {
    if (creating) {
      creatingCanvas.current.className = 'absolute inset-0 bg-transparent z-[99]'
      creatingShape.current.className = 'absolute bg-gray-800 bg-opacity-30 border-gray-900 border'
    } else {
      creatingCanvas.current.className = 'hidden'
      creatingShape.current.className = 'hidden'
    }
  },[creating])

  useEffect(()=>{
    console.log(props.containerRef.current.getBoundingClientRect())
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
