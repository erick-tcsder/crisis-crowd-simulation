import { useEffect, useRef } from "react";
import streamsaver from 'streamsaver'

export const useStreamingAssets = (loading,maps,simulationProps,onNewState,onStreamingEnd= ()=>{console.log('ENDED')},filename = 'simulation',) => {
  const positions = useRef([])
  useEffect(() => {
    const eventSource = new EventSource("http://localhost:8000/simulation/stream",{withCredentials:false})
    const fileSaver = streamsaver.createWriteStream(`${filename}.json`)
      let writer = fileSaver.getWriter()
      let wroted = false
      const encode = TextEncoder.prototype.encode.bind(new TextEncoder())
      writer.write(encode(`{\n"simulationProps":${JSON.stringify(simulationProps)},\n"maps": ${JSON.stringify(maps)},\n"positions": [\n`))
      eventSource.onmessage = (event) => {
        if(JSON.parse(event.data) === 'end'){
          onStreamingEnd?.()
          writer.write(encode('],\n "end": true\n}'))
          writer.close()
          eventSource.close()
          return
        }
        positions.current.push(JSON.parse(event.data))
        onNewState?.(JSON.parse(event.data))
        writer.write(encode(`${wroted ? ',\n' : ''}${JSON.stringify(JSON.parse(event.data).ped)}`))
        wroted = true
      };
      eventSource.onerror = (err)=>{
        writer.write(encode(`],\n "end": false,\n "error": ${JSON.stringify(err)}\n}`))
        writer.close()
        eventSource.close()
      }
  
      return ()=>{
        writer.write(encode('],\n "end": false,\n "error": "closed by user"\n}'))
        writer.close()
        eventSource.close()
      }
  }, []);

  return {
    positions: positions.current
  }
}

export const useStreamingVuln = (loading,maps,vulnerabilityProps,onNewState,onStreamingEnd= ()=>{console.log('ENDED')},filename = 'vulnerabilities',) => {
  const events = useRef([])
  useEffect(() => {
    const eventSource = new EventSource("http://localhost:8000/vulnerabilities/stream",{withCredentials:false})
    const fileSaver = streamsaver.createWriteStream(`${filename}.json`)
      let writer = fileSaver.getWriter()
      let wroted = false
      const encode = TextEncoder.prototype.encode.bind(new TextEncoder())
      writer.write(encode(`{\n"vulnerabilityProps":${JSON.stringify(vulnerabilityProps)},\n"maps": ${JSON.stringify(maps)},\n"events": [\n`))
      eventSource.onmessage = (event) => {
        if(JSON.parse(event.data) === 'end'){
          onStreamingEnd?.()
          writer.write(encode('],\n "end": true\n}'))
          writer.close()
          eventSource.close()
          return
        }
        events.current.push(JSON.parse(event.data))
        onNewState?.(JSON.parse(event.data))
        writer.write(encode(`${wroted ? ',\n' : ''}${JSON.stringify(JSON.parse(event.data))}`))
        wroted = true
      };
      eventSource.onerror = (err)=>{
        writer.write(encode(`],\n "end": false,\n "error": ${JSON.stringify(err)}\n}`))
        writer.close()
        eventSource.close()
      }
  
      return ()=>{
        writer.write(encode('],\n "end": false,\n "error": "closed by user"\n}'))
        writer.close()
        eventSource.close()
      }
  }, []);

  return {
    events: events.current
  }
}
