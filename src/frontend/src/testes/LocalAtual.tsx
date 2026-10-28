import { useLocation } from 'react-router'

function LocalAtual() {
  const { pathname, search } = useLocation()
  return <output data-testid="local">{`${pathname}${search}`}</output>
}

export default LocalAtual
