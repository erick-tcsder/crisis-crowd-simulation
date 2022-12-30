import axios from 'axios';

export class SimulationService{
  static get axios(){
    const instance = axios.create({
      baseURL: 'http://localhost:8000',
    })
    return instance
  }

  static async restartSimulation(){
    return await SimulationService.axios.post('/simulation/restart');
  }

  static async startSimulation(){
    return await SimulationService.axios.post('/simulation/start');
  }

  static async stopSimulation(){
    return await SimulationService.axios.post('/simulation/stop');
  }

  static async getSimulationStatus(){
    return await SimulationService.axios.get('/simulation/status');
  }

  static async addMap(map){
    return await SimulationService.axios.post('/map',map);
  }

  static async getMaps(){
    return await SimulationService.axios.get('/map');
  }

  static async getMap(id){
    return await SimulationService.axios.get(`/map/${id}`);
  }

  static async deleteMap(id){
    return await SimulationService.axios.delete(`/map/${id}`);
  }
}