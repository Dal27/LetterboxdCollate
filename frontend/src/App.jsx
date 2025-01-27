import './App.css'


import Films from './components/Films';

function App() {

  return (
    <>
      <div className="absolute sm:inset-y-1/3 sm:left-1/10 sm:w-40 inset-x-0 bottom-20 mb-20 text-center">
        <nav>
          <ul>
            <li className="text-pinky"><a href="#">Recommend Films</a></li>
            <li className="text-greeny"><a href="#">Compare w/ Friends</a></li>
            <li className="text-bluey"><a href="#">About</a></li>
          </ul>
        </nav>
      </div>
      
      <Films />

      <div className="zig-zag absolute inset-x-0 bottom-0 h-16">
        <p className="m-5 absolute inset-x-0 bottom-0 text-center text-sm text-purpley">
            Nayan
        </p>
      </div>

      </>
  )
}

export default App
