from typing import List
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse,RedirectResponse
import json
from simulation.environment.blueprint import Blueprint, DamageZone
from pydantic import BaseModel
import asyncio
from simulation.context import Pedestrian, SimulationContext
import numpy as np
import time

app = FastAPI(debug=True)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class JsonBluePrint(BaseModel):
  name: str
  width: int
  height: int
  items: List[dict]
  
class SimulationStart(BaseModel):
  agentCount: int
  explosionDeathRadius: float
  explosionFloorName: str
  explosionTop: float
  explosionLeft: float
  
class VulnerabilityStart(BaseModel):
  agentCount: int
  explosionDeathRadius: float

simulationBuilding:List[Blueprint] = []
simulationStatus = "SETTING UP"

simulationContext : SimulationContext = None

@app.get('/')
def main():
  return RedirectResponse('/docs')

@app.post('/simulation/restart')
def restartSimulation():
  simulationBuilding.clear()
  return 'OK'

@app.get('/map')
def getMap():
  return [i.toJson() for i in simulationBuilding]

@app.get('/map/{name}')
def getMapByName(name:str):
  for i in simulationBuilding:
    if i.name == name:
      return i.toJson()
  return 'Not Found',404

@app.post('/map')
def addMap(map:JsonBluePrint):
  if len(simulationBuilding) > 0:
    return 'Map already exists',400
  if simulationStatus == "RUNNING" :
    return 'Simulation is running',400
  if map.name in [i.name for i in simulationBuilding]:
    simulationBuilding.remove([i for i in simulationBuilding if i.name == map.name][0])
  simulationBuilding.append(Blueprint.fromJson(map))
  return 'OK'
  
@app.delete('/map/{name}')
def deleteMapByName(name:str):
  if simulationStatus == "RUNNING" :
    return 'Simulation is running',400
  for i in simulationBuilding:
    if i.name == name:
      simulationBuilding.remove(i)
      return 'OK'
  return 'Not Found',404

@app.get('/simulation/status')
def getSimulationStatus():
  status = {
    "status": simulationStatus  
  }
  return status

@app.post('/simulation/start')
def simulationStart(data:SimulationStart):
  global simulationStatus
  simulationStatus = 'RUNNING'
  building = simulationBuilding[0]
  start = (data.explosionLeft - data.explosionDeathRadius/2,data.explosionTop - data.explosionDeathRadius/2)
  end = (data.explosionLeft + data.explosionDeathRadius/2,data.explosionTop + data.explosionDeathRadius/2)
  damageZone = DamageZone([start,end],0.9)
  building.objects.append(damageZone)
  a = 123
  global simulationContext
  simulationContext = SimulationContext(building)
  simulationContext.setup_navmesh()
  simulationContext.setup_pdestrians(data.agentCount, 123)
  simulationContext.setup_routes(123)
  return {
    'status': simulationStatus
  }

@app.post('/vulnerability/start')
def vulnerabilityStart(data:VulnerabilityStart):
  #TODO: do somthing with maps and incoming data
  return 'OK'

@app.post('/simulation/stop')
def simulationStop():
  simulationStatus = 'STOPPED'
  return 'OK'

async def stream_simulation():
  if simulationStatus != 'RUNNING':
    yield f"data: {json.dumps('end')}\n\n"
  ticks = 0
  tickInterval = 0.5
  initTime = time.time()
  while True:
    simulationContext.update()
    if time.time() - initTime > tickInterval*ticks:
      await asyncio.sleep(0.1)
      ticks += 1
      data : List[Pedestrian] = np.copy(simulationContext.agents)
      jsonedData = {'ped':[i.toJson() for i in data]}
      yield f"data: {json.dumps(jsonedData)}\n\n"
  yield f"data: {json.dumps('end')}\n\n"

async def stream_vulnerabilities():
  i = 0
  while True:
    if i == 10: break
    yield f"data: {json.dumps({'bar': i})}\n\n"
    i += 1
    await asyncio.sleep(0.25)
  yield f"data: {json.dumps('end')}\n\n"

@app.get("/simulation/stream")
async def streamSim():
  return StreamingResponse(stream_simulation(), media_type="text/event-stream")

@app.get("/vulnerabilities/stream")
def streamVul():
  return StreamingResponse(stream_vulnerabilities(), media_type="text/event-stream")