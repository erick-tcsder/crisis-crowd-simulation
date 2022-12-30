import { useCallback } from "react"
import { Button } from "./Button"
import classNames from "classnames"
import {useNavigate} from 'react-router-dom'
import { SimulationService } from "../hooks/simulationservice"

export const ToolsSection = ({setCreating,creating, map, setMap,...props}) => {
  const navigator = useNavigate()
  const handleCreateObj = useCallback((obj)=>{
    setCreating(obj)
  },[setCreating])
  return (
    <div className="flex flex-col h-full pb-5 select-none">
      <div className="">
        <input value={map?.name} onChange={(e)=>setMap(map => ({
          ...map,
          name: e.target.value,
        }))} placeholder={'Map Name'} required type='text' className="form-input text-white px-3 py-2 bg-[#232639] rounded-md w-full"/>
      </div>

      <span className="mt-5 mb-1 uppercase text-xs opacity-50">Obstacles</span>
      <div className="flex flex-row justify-start gap-3">
      <Button onClick={()=>handleCreateObj('RECTANGULAR_OBSTACLE')} icon={classNames({'bi bi-square':creating!== 'RECTANGULAR_OBSTACLE','bi bi-square-fill': creating === 'RECTANGULAR_OBSTACLE'})} className={classNames({
          'rounded-md px-3 py-2':true,
          'bg-sky-500 text-white':creating==='RECTANGULAR_OBSTACLE',
          'ring-2 ring-sky-500 text-sky-500 hover:bg-sky-400 hover:bg-opacity-30 ring-inset': creating !== 'RECTANGULAR_OBSTACLE'
        })}>Rect</Button>
        <Button onClick={()=>handleCreateObj('CIRCLE_OBSTACLE')} icon={classNames({'bi bi-circle':creating!== 'CIRCLE_OBSTACLE','bi bi-circle-fill': creating === 'CIRCLE_OBSTACLE'})} className={classNames({
          'rounded-md px-3 py-2':true,
          'bg-sky-500 text-white':creating==='CIRCLE_OBSTACLE',
          'ring-2 ring-sky-500 text-sky-500 hover:bg-sky-400 hover:bg-opacity-30 ring-inset': creating !== 'CIRCLE_OBSTACLE'
        })}>Circle</Button>
      </div>

      <span className="mt-5 mb-1 uppercase text-xs opacity-50">Signs</span>
      <div className="flex flex-row justify-start gap-3">
        <Button onClick={()=>handleCreateObj('UP')} icon={'bi bi-arrow-up'} className={classNames({
            'rounded-md px-3 py-2':true,
            'bg-sky-500 text-white':creating==='UP',
            'ring-2 ring-sky-500 text-sky-500 hover:bg-sky-400 hover:bg-opacity-30 ring-inset': creating !== 'UP'
          })}/>
        <Button onClick={()=>handleCreateObj('RIGHT')} icon={'bi bi-arrow-right'} className={classNames({
            'rounded-md px-3 py-2':true,
            'bg-sky-500 text-white':creating==='RIGHT',
            'ring-2 ring-sky-500 text-sky-500 hover:bg-sky-400 hover:bg-opacity-30 ring-inset': creating !== 'RIGHT'
          })}/>
        <Button onClick={()=>handleCreateObj('DOWN')} icon={'bi bi-arrow-down'} className={classNames({
            'rounded-md px-3 py-2':true,
            'bg-sky-500 text-white':creating==='DOWN',
            'ring-2 ring-sky-500 text-sky-500 hover:bg-sky-400 hover:bg-opacity-30 ring-inset': creating !== 'DOWN'
          })}/>
        <Button onClick={()=>handleCreateObj('LEFT')} icon={'bi bi-arrow-left'} className={classNames({
            'rounded-md px-3 py-2':true,
            'bg-sky-500 text-white':creating==='LEFT',
            'ring-2 ring-sky-500 text-sky-500 hover:bg-sky-400 hover:bg-opacity-30 ring-inset': creating !== 'LEFT'
          })}/>
      </div>

      <span className="mt-5 mb-1 uppercase text-xs opacity-50">Miscellaneous</span>
      <div className="flex flex-row justify-start gap-3 flex-wrap">
        <Button onClick={()=>handleCreateObj('DOOR')} icon={classNames({'bi bi-door-open':creating!== 'DOOR','bi bi-door-open-fill': creating === 'DOOR'})} className={classNames({
            'rounded-md px-3 py-2':true,
            'bg-sky-500 text-white':creating==='DOOR',
            'ring-2 ring-sky-500 text-sky-500 hover:bg-sky-400 hover:bg-opacity-30 ring-inset': creating !== 'DOOR'
          })}>Door</Button>
        <Button onClick={()=>handleCreateObj('SAFE_ZONE')} icon={classNames({'bi bi-heart':creating!== 'SAFE_ZONE','bi bi-heart-fill': creating === 'SAFE_ZONE'})} className={classNames({
            'rounded-md px-3 py-2':true,
            'bg-sky-500 text-white':creating==='SAFE_ZONE',
            'ring-2 ring-sky-500 text-sky-500 hover:bg-sky-400 hover:bg-opacity-30 ring-inset': creating !== 'SAFE_ZONE'
          })}>Safe Zone</Button>
        <Button onClick={()=>handleCreateObj('EXIT')} icon={'bi bi-box-arrow-right'} className={classNames({
          'rounded-md px-3 py-2':true,
          'bg-sky-500 text-white':creating==='EXIT',
          'ring-2 ring-sky-500 text-sky-500 hover:bg-sky-400 hover:bg-opacity-30 ring-inset': creating !== 'EXIT'
        })}>Evacuation Exit</Button>
        <Button onClick={()=>handleCreateObj('STAIRS')} icon={'bi bi-reception-4'} className={classNames({
          'rounded-md px-3 py-2':true,
          'bg-sky-500 text-white':creating==='STAIRS',
          'ring-2 ring-sky-500 text-sky-500 hover:bg-sky-400 hover:bg-opacity-30 ring-inset': creating !== 'STAIRS'
        })}>Stairs</Button>
        <Button onClick={()=>handleCreateObj('ELEVATOR')} icon={'bi bi-arrow-down-up'} className={classNames({
          'rounded-md px-3 py-2':true,
          'bg-sky-500 text-white':creating==='ELEVATOR',
          'ring-2 ring-sky-500 text-sky-500 hover:bg-sky-400 hover:bg-opacity-30 ring-inset': creating !== 'ELEVATOR'
        })}>Elevator</Button>
      </div>

      <span className="mt-5 mb-1 uppercase text-xs opacity-50">Damage</span>
      <div className="flex flex-row justify-start g ap-3">
        <Button onClick={()=>handleCreateObj('DAMAGE_ZONE')} icon={'bi bi-fire'} className={classNames({
          'rounded-md px-3 py-2':true,
          'bg-red-500 text-white':creating==='DAMAGE_ZONE',
          'ring-2 ring-red-500 text-red-500 hover:bg-red-400 hover:bg-opacity-30 ring-inset': creating !== 'DAMAGE_ZONE'
        })}>Damage Zone</Button>
      </div>

      <div className="mt-auto flex px-3 justify-evenly">
      <Button onClick={()=>navigator('/')} icon={'bi bi-x'} className={classNames({
          'rounded-md px-3 py-2':true,
          'ring-2 ring-sky-500 text-sky-500 hover:bg-sky-400 hover:bg-opacity-30 ring-inset': true
        })}>Cancel</Button>
      <Button onClick={async()=>{
        try{
          await SimulationService.addMap(map)
        }catch(e){

        }
        navigator('/')
      }} icon={'bi bi-save2'} className={classNames({
          'rounded-md px-3 py-2':true,
          'bg-sky-500 text-white hover:ring-sky-300 hover:ring-2 hover:ring-offset-2 hover:ring-offset-[#121425]':true,
        })}>Save</Button>
      </div>
    </div>
  )
}