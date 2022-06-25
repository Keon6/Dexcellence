import logo from './logo.svg';
import ActionCard from './components/ActionCard.js'
import './App.css';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <div className="App-topbar">
          <Navbar></Navbar>
        </div>
        <div className="App-main-box">
          <p className="Actions">Actions</p>
          <ActionCard></ActionCard>
        </div>
      </header>
    </div>
  );
}

export default App;
