import { Portal } from "./portal"

export const PageTitle = ({title}) => {
  return <Portal portalName={'page-title-portal'}>
    <h1 className="text-3xl font-bold text-sky-400">
      {title}
    </h1>
  </Portal>
}