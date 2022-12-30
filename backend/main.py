from typing import List
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core import Blueprint
from pydantic import BaseModel

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
  simulationBuilding = []
  return 'OK',200

@app.get('/map')
def getMap():
  return [i.toJson() for i in simulationBuilding]

@app.get('/map/{name}')
def getMapByName(name:str):
  for i in simulationBuilding:
    if i.name == name:
      return i.toJson(),200
  return 'Not Found',404

@app.post('/map')
def addMap(map:JsonBluePrint):
  if simulationStatus == "RUNNING" :
    return 'Simulation is running',400
  simulationBuilding.append(Blueprint.fromJson(map))
  return 'OK',200
  
@app.delete('/map/{name}')
def deleteMapByName(name:str):
  if simulationStatus == "RUNNING" :
    return 'Simulation is running',400
  for i in simulationBuilding:
    if i.name == name:
      simulationBuilding.remove(i)
      return 'OK',200
  return 'Not Found',404

@app.get('/simulation/status')
def getSimulationStatus():
  status = {
    "status": simulationStatus  
  }
  if simulationStatus == 'RUNNING' :
    status.conection = '8080'
  return status,200

@app.post('/simulation/start')
def simulationStart():
  simulationStatus = 'RUNNING'
  return 'OK',200

@app.post('/simulation/stop')
def simulationStop():
  simulationStatus = 'STOPPED'
  return 'OK',200