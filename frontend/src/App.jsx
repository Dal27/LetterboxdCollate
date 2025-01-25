import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'

import Films from './components/Films';

function App() {

  return (
    <>
      <div>
        <a href="https://vite.dev" target="_blank">
          <img src={viteLogo} className="logo" alt="Vite logo" />
        </a>
        <a href="https://react.dev" target="_blank">
          <img src={reactLogo} className="logo react" alt="React logo" />
        </a>
      </div>
      <h1>Letterboxd Collator</h1>

      <Films />

      <div className="card">
        
        <p>
        </p>
      </div>
      <p className="read-the-docs">
        Nayan
      </p>
    </>
  )
}

export default App
