import React, {useRef, useEffect } from 'react';
import Swal from 'sweetalert2'
import { SimulationService } from '../hooks/simulationservice';
import {useNavigate} from 'react-router-dom'

function DragAndDropOverlay() {
  const overlayRef = useRef(null)
  const ovChild = useRef(null)
  const navigator = useNavigate()
  
  useEffect(() => {
    const overlay = overlayRef.current;
    const ovBox = ovChild.current;
    const handleDragEnter = (event) => {
      overlay.style.display = 'flex'
      event.preventDefault();
    };
  
    const handleDragLeave = (event) => {
      event.preventDefault();
      overlay.style.display = 'none'
    };
  
    const handleDrop = async (event) => {
      event.preventDefault();
      const file = event.dataTransfer.files[0];
      overlay.style.display = 'none'

      if (file.type !== 'application/json') {
        Swal.fire({
          title: 'Invalid file type',
          icon: 'error',
        })
        return;
      }
      const reader = new FileReader();
      reader.onload = async(event) => {
        const data = JSON.parse(event.target.result);
        await SimulationService.addMap(data)
        navigator(0)
      };
      reader.readAsText(file);
    };
    window.addEventListener('dragenter', handleDragEnter);
    overlay.addEventListener('dragleave', handleDragLeave);
    overlay.addEventListener('dragover', handleDragEnter);
    overlay.addEventListener('drop', handleDrop);
    ovBox.addEventListener('dragleave', handleDragLeave);
    ovBox.addEventListener('dragover', handleDragEnter);
    ovBox.addEventListener('drop', handleDrop);

    return () => {
      window.removeEventListener('dragenter', handleDragEnter);
      ovBox.removeEventListener('dragleave', handleDragLeave);
      ovBox.removeEventListener('dragover', handleDragEnter);
      ovBox.removeEventListener('drop', handleDrop);
      overlay.removeEventListener('dragleave', handleDragLeave);
      overlay.removeEventListener('dragover', handleDragEnter);
      overlay.removeEventListener('drop', handleDrop);
    };
  },[])

  return (
    <div>
      <div
        ref={overlayRef}
        style={{
          position: 'fixed',
          top: 0,
          left: 0,
          right: 0,
          bottom: 0,
          backgroundColor: 'rgba(0, 0, 0, 0.5)',
          display: 'none',
          alignItems: 'center',
          justifyContent: 'center',
          flexDirection: 'column',
        }}
        className='z-[999]'
      >
        <div className='p-36 border-2 border-sky-400 text-sky-400 bg-sky-400 bg-opacity-20 rounded-3xl border-dashed' ref={ovChild} style={{ color: 'white' }}>
          Drop the file here to upload it
        </div>
      </div>
    </div>
  );
}

export default DragAndDropOverlay;