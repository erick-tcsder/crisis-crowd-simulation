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
from simulation.events import *
from simulation.metaheuristic import vulnerability_data

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
  explosionDeathRadius: float


simulationBuilding: List[Blueprint] = []
simulationStatus = "SETTING UP"

simulationContext: SimulationContext = None


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
def getMapByName(name: str):
  for i in simulationBuilding:
    if i.name == name:
      return i.toJson()
  return 'Not Found', 404


@app.post('/map')
def addMap(map: JsonBluePrint):
  if len(simulationBuilding) > 0:
    return 'Map already exists', 400
  if simulationStatus == "RUNNING":
    return 'Simulation is running', 400
  if map.name in [i.name for i in simulationBuilding]:
    simulationBuilding.remove(
        [i for i in simulationBuilding if i.name == map.name][0])
  simulationBuilding.append(Blueprint.fromJson(map))
  return 'OK'


@app.delete('/map/{name}')
def deleteMapByName(name: str):
  if simulationStatus == "RUNNING":
    return 'Simulation is running', 400
  for i in simulationBuilding:
    if i.name == name:
      simulationBuilding.remove(i)
      return 'OK'
  return 'Not Found', 404


@app.get('/simulation/status')
def getSimulationStatus():
  status = {
      "status": simulationStatus
  }
  return status


@app.post('/simulation/start')
def simulationStart(data: SimulationStart):
  global simulationStatus
  simulationStatus = 'RUNNING'
  building = simulationBuilding[0]
  start = (data.explosionLeft - data.explosionDeathRadius/2,
           data.explosionTop - data.explosionDeathRadius/2)
  end = (data.explosionLeft + data.explosionDeathRadius/2,
         data.explosionTop + data.explosionDeathRadius/2)
  damageZone = DamageZone([start, end], 0.9)
  building.objects.append(damageZone)
  a = 123
  global simulationContext
  simulationContext = SimulationContext(building)
  simulationContext.setup_navmesh()
  simulationContext.setup_pedestrians(data.agentCount, 123)
  simulationContext.setup_routes(123)
  return {
      'status': simulationStatus
  }


@app.post('/vulnerability/start')
def vulnerabilityStart(data: VulnerabilityStart):
  global vuln_radius
  vuln_radius = data.explosionDeathRadius
  return 'OK'


@app.post('/simulation/stop')
def simulationStop():
  global simulationStatus
  global simulationContext
  simulationStatus = 'STOPPED'
  simulationContext = None
  return 'OK'

async def stream_simulation_x1():
  if simulationStatus != 'RUNNING':
    yield f"data: {json.dumps('end')}\n\n"
  cycles = 0
  waitInterval = 0.0625
  simultionInterval = 0.125
  lasCycleTime = time.time()
  while True:
    if simulationStatus == 'STOPPED':
      break
    cycles += 1
    ended = simulationContext.update()
    await asyncio.sleep(max(waitInterval - time.time() + lasCycleTime,0.01))
    lasCycleTime = time.time()
    data: List[Pedestrian] = np.copy(simulationContext.agents)
    jsonedData = {'ped': [i.toJson() for i in data],
                  'time': cycles * simultionInterval}
    yield f"data: {json.dumps(jsonedData)}\n\n"
    if ended: break
  await asyncio.sleep(0.1)
  yield f"data: {json.dumps('end')}\n\n"


async def stream_vulnerabilities():
  stream = (candidates for _,
            candidates in vulnerability_data(
                simulationBuilding[0],
                vuln_radius))
  initTime = time.time()
  geneticIterations = 0
  maxGeneticIterations = 100
  maxTime = 1200 #20 mins max
  while True:
    if geneticIterations >= maxGeneticIterations or time.time() - initTime >= maxTime:
      break
    #Send Initialization of a genetic Iteration
    await asyncio.sleep(0.1)
    yield f"data: {json.dumps(LogEvent(f'Genetic Iteration {geneticIterations} STARTED').toJson())}\n\n"
    #call the genetic iteration
    r = next(stream)
    #show results
    #...
  #Send ResultEvent + EndEvent
  await asyncio.sleep(0.1)
  yield f"data: {json.dumps(ResultEvent(f'Best Result after {geneticIterations} genetic Iterations',{'bestPlaces': [{'top':c.y,'left':c.x} for c in r]}).toJson())}\n\n"
  await asyncio.sleep(0.1)
  yield f"data: {json.dumps(EndEvent('Vulnerabilities Check Ended',None).toJson())}\n\n"
  await asyncio.sleep(0.1)
  yield f"data: {json.dumps('end')}\n\n"

@app.get("/simulation/stream")
async def streamSim():
  return StreamingResponse(stream_simulation_x1(), media_type="text/event-stream")

@app.get("/vulnerabilities/stream")
def streamVul():
  return StreamingResponse(stream_vulnerabilities(), media_type="text/event-stream")