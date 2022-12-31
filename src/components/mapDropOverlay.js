export const MapDropOverlay = ()=>{
  return (
    <div className='fixed inset-5 flex'>
      <div className='flex flex-col m-auto'>
        <i className="bi bi-save"/>
        <span>Drop maps to directly import it</span>
      </div>
      <div className='blur-3xl bg-sky-400 opacity-25 aspect-square w-80 rounded-full fixed left-1/2 top-1/2'/>
    </div>
  )
}