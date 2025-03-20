import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.jsx'
import LinearProgrammingSolver from './linearSolver.jsx'

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <LinearProgrammingSolver />
  </StrictMode>,
)
