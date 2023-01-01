import { useEffect, useRef } from "react";
import streamsaver from 'streamsaver'

export const useStreamingAssets = (loading,maps,simulationProps,onNewState,onStreamingEnd= ()=>{console.log('ENDED')},filename = 'simulation',) => {
  const positions = useRef([])
  useEffect(() => {
    if(!loading && maps.length > 0 && simulationProps && simulationProps?.peopleCount){
      let fileSaver = streamsaver.createWriteStream(`${filename}.json`)
      let writer = fileSaver.getWriter()
      let wroted = false
      const encode = TextEncoder.prototype.encode.bind(new TextEncoder())
      writer.write(encode(`{\n"simulationProps":${JSON.stringify(simulationProps)},\n"maps": ${JSON.stringify(maps)},\n"positions": [\n`))
      const eventSource = new EventSource("http://localhost:8000/stream",{withCredentials:false});
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
        writer.write(encode(`${wroted ? ',\n' : ''}${event.data}`))
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
    }
  }, [filename, loading, maps, simulationProps]);

  return {
    positions: positions.current
  }
}
