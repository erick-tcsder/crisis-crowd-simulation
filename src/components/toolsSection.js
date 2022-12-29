import { useCallback } from "react"

export const ToolsSection = ({setCreating,creating,...props}) => {
  const handleCreateObj = useCallback((obj)=>{
    setCreating(obj)
  },[setCreating])
  return (
    <div className="flex flex-col">
      <div>Input MAP NAME</div>

      <span>Walls</span>
      <div className="flex flex-row justify-start gap-3">
        <button onClick={()=>handleCreateObj('VWALL')}>VWALL </button>
        <button onClick={()=>handleCreateObj('HWALL')}>HWALL</button>
      </div>

      <span>Obstacles</span>
      <div className="flex flex-row justify-start gap-3">
        <button onClick={()=>handleCreateObj('RECT')}>RECT </button>
        <button onClick={()=>handleCreateObj('CIRC')}>CIRC</button>
      </div>

      <span>Signs</span>
      <div className="flex flex-row justify-start gap-3">
        <button onClick={()=>handleCreateObj('UP')}>UP </button>
        <button onClick={()=>handleCreateObj('RIGHT')}>RIGHT</button>
        <button onClick={()=>handleCreateObj('DOWN')}>DOWN </button>
        <button onClick={()=>handleCreateObj('LEFT')}>LEFT</button>
      </div>

      <span>Miscellaneous</span>
      <div className="flex flex-row justify-start gap-3">
        <button onClick={()=>handleCreateObj('DOOR')}>DOOR</button>
        <button onClick={()=>handleCreateObj('SAFE')}>SAFE</button>
        <button onClick={()=>handleCreateObj('EXIT')}>EXIT</button>
        <button onClick={()=>handleCreateObj('STAIRS')}>STAIRS</button>
        <button onClick={()=>handleCreateObj('ELEVATOR')}>ELEVATOR </button>
      </div>

      <div className="grid grid-cols-2">
        <button className="">Cancel</button>
        <button className="">Save</button>
      </div>
    </div>
  )
}