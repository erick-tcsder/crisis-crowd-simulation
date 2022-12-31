from typing import List
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
import json
from core import Blueprint
from pydantic import BaseModel
import asyncio

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

simulationBuilding:List[Blueprint] = []
simulationStatus = "SETTING UP"

@app.get('/')
def main():
  return 'Hello World!!!'

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
  if simulationStatus == 'RUNNING' :
    status.conection = '8080'
  return status

@app.post('/simulation/start')
def simulationStart():
  simulationStatus = 'RUNNING'
  return 'OK'

@app.post('/simulation/stop')
def simulationStop():
  simulationStatus = 'STOPPED'
  return 'OK'

async def stream_foo():
  i = 0
  while True:
    if i == 10: break
    yield f"data: {json.dumps({'foo': i})}\n\n"
    i += 1
    await asyncio.sleep(0.5)
  yield f"data: {json.dumps('end')}\n\n"

@app.get("/stream")
async def stream():
  return StreamingResponse(stream_foo(), media_type="text/event-stream")