import { useEffect, useRef, useState } from 'react';
import ReactDOM from 'react-dom';

export const Portal = ({
  children,
  portalName,
}) => {
  const [mounted, setMounted] = useState(false);
  const ref = useRef(null);

  useEffect(() => {
    ref.current = document.querySelector(`#${portalName}`);
    setMounted(true);

    return () => setMounted(false);
  }, [portalName]);

  return mounted && ref.current
    ? ReactDOM.createPortal(children, ref.current, portalName)
    : null;
};
