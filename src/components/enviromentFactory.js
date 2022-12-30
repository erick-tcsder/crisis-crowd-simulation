import { Utils } from "../utils";

export const envMapper = {
  RECTANGULAR_OBJ: (props)=>{
    return (
      <div
        className="absolute bg-gray-800 bg-opacity-30 border-gray-900 border"
        style={{
          top: Utils.getMToPx(props.map, props.canvas, props.top),
          left: Utils.getMToPx(props.map, props.canvas, props.left),
          width: Utils.getMToPx(props.map, props.canvas, props.width),
          height: Utils.getMToPx(props.map, props.canvas, props.height),
        }}
      ></div>
    )
  },
  CIRCULAR_OBJ: (props)=>{
    return (
      <div
        className="absolute bg-gray-800 bg-opacity-30 border-gray-900 border aspect-square"
        style={{
          top: Utils.getMToPx(props.map, props.canvas, props.top),
          left: Utils.getMToPx(props.map, props.canvas, props.left),
          width: Utils.getMToPx(props.map, props.canvas, props.radius),
          height: Utils.getMToPx(props.map, props.canvas, props.radius),
          borderRadius: '50%'
        }}
      ></div>
    )
  },
  STAIRS: (props)=>{
    return (
      <div
        className="absolute bg-orange-400 bg-opacity-30 text-orange-700 border-orange-500 border-2 grid place-content-center"
        style={{
          top: Utils.getMToPx(props.map, props.canvas, props.top),
          left: Utils.getMToPx(props.map, props.canvas, props.left),
          width: Utils.getMToPx(props.map, props.canvas, props.width),
          height: Utils.getMToPx(props.map, props.canvas, props.height),
        }}
      >{props.label}</div>
    )
  },
  DOOR:(props)=>{
    return (
      <div
        className="absolute bg-purple-600 bg-opacity-30 border-purple-700 border-2 grid place-content-center"
        style={{
          top: Utils.getMToPx(props.map, props.canvas, props.top),
          left: Utils.getMToPx(props.map, props.canvas, props.left),
          width: Utils.getMToPx(props.map, props.canvas, props.width),
          height: Utils.getMToPx(props.map, props.canvas, props.height),
        }}
      ></div>
    )
  },
  ELEVATOR: (props)=>{
    return (
      <div
        className="absolute bg-indigo-400 bg-opacity-30 text-indigo-800 border-indigo-500 border-2 grid place-content-center"
        style={{
          top: Utils.getMToPx(props.map, props.canvas, props.top),
          left: Utils.getMToPx(props.map, props.canvas, props.left),
          width: Utils.getMToPx(props.map, props.canvas, props.width),
          height: Utils.getMToPx(props.map, props.canvas, props.height),
        }}
      >{props.label}</div>
    )
  },
  SAFE_ZONE: (props)=>{
    return (
      <div
        className="absolute bg-lime-400 bg-opacity-30 border-lime-500 border-2 grid place-content-center"
        style={{
          top: Utils.getMToPx(props.map, props.canvas, props.top),
          left: Utils.getMToPx(props.map, props.canvas, props.left),
          width: Utils.getMToPx(props.map, props.canvas, props.width),
          height: Utils.getMToPx(props.map, props.canvas, props.height),
        }}
      ></div>
    )
  },
  EVAC_EXIT: (props)=>{
    return (
      <div
        className="absolute bg-green-400 bg-opacity-30 border-green-500 border-2 grid place-content-center"
        style={{
          top: Utils.getMToPx(props.map, props.canvas, props.top),
          left: Utils.getMToPx(props.map, props.canvas, props.left),
          width: Utils.getMToPx(props.map, props.canvas, props.width),
          height: Utils.getMToPx(props.map, props.canvas, props.height),
        }}
      ></div>
    )
  },
  DAMAGE_ZONE: (props)=>{
    return (
      <div
        className="absolute bg-red-500 bg-opacity-30 border-red-500 border-2 grid place-content-center"
        style={{
          top: Utils.getMToPx(props.map, props.canvas, props.top),
          left: Utils.getMToPx(props.map, props.canvas, props.left),
          width: Utils.getMToPx(props.map, props.canvas, props.width),
          height: Utils.getMToPx(props.map, props.canvas, props.height),
        }}
      ></div>
    )
  },
  EVAC_SIGN: (props)=>{
    return (
      <div
        className="absolute bg-yellow-500 bg-opacity-30 text-yellow-800 border-yellow-500 border-2 grid place-content-center"
        style={{
          top: Utils.getMToPx(props.map, props.canvas, props.top),
          left: Utils.getMToPx(props.map, props.canvas, props.left),
          width: Utils.getMToPx(props.map, props.canvas, props.width),
          height: Utils.getMToPx(props.map, props.canvas, props.height),
        }}
      >
        <i className={`bi bi-arrow-${props.direction}`}/>
      </div>
    )
  },
};

export const EnviromentFactory = ({
  envOjb,
  enviromentMapper,
  canvas,
  map,
}) => {
  if(!canvas) return <></>
  const Component = enviromentMapper[envOjb?.["OBJECT_TYPE"]];
  return <Component {...envOjb.props} canvas={canvas} map={map} />;
};
