import logo from './logo.svg';
import './App.css';
import Select from 'react-dropdown-select'
import {useState} from 'react';

function App(props) {
  var coins = [
    { value: 'btc', label: 'BTC' },
    { value: 'eth', label: 'ETH' },
    { value: 'sol', label: 'SOL' },
  ]

  const [numCards, setNumCards] = useState(0);
  const [cards, setCards] = useState([]);

  const addCard = i => {
    const newCards = [...cards, {
      'index' : numCards,
      'action' : 'buy',
      'coin' : 'eth',
      'mmp' : 0,
      'ttxa' : 0,
    }];
    setNumCards(numCards + 1);
    setCards(newCards);
  }

  const updateOrder = (index, field, value) => {
    const newCards = [...cards];
    newCards[index][field] = value;
    console.log("Set order[" + index + "]." + field + " to " + value);
    setCards(newCards);
  }

  function removeActionCard(index) {
    const newCards = [...cards];
    for (var start = index + 1; start < newCards.length; start++) {
      newCards[start].index -= 1;
    }
    newCards.splice(index, 1);
    setCards(newCards);
    setNumCards(numCards - 1);
  }

  return (
    <div className="App">
      <header className="App-header">
        <div className="App-topbar">
          {/*<Navbar></Navbar>*/}
        </div>
        <div className="App-main-box">
          <p className="Actions">Place a Complex Order</p>
          <div className = "ActionCardContainer">
            {
              cards.map((order, index) => (
                <div className = "ActionCard-box">
                  <div className = "ActionCard-spacer"></div>
                  <p className = "IndexText">{index}</p>
                  <div className = "ActionCard-spacer"></div>
                  {/*Input the action (buy/sell)*/}
                  <div className = "InputItem-flex">
                      <select 
                          value={order.action} 
                          onChange={e => updateOrder(index, 'action', e.target.value)} 
                          className = "InputItem-dropdown">
                          <option value="Buy">Buy</option>
                          <option value="Sell">Sell</option>
                      </select>
                      <p className = "InputItem-text">Action</p>
                  </div>
                  <div className = "ActionCard-spacer"></div>
                  {/*Input the coin*/}
                  <div className = "InputItem-flex">
                      <Select
                          options = {coins}
                          placeholder = 'ETH'
                          color = 'white'
                          onChange = {(values) => updateOrder(index, 'coin', values[0].label)}
                          className = "InputItem-dropdown"
                          style = {{width: '100px', 
                          borderRadius: '5px',
                          border: '1px solid white',}}
                          searchable = {false}  
                      />
                      <p className = "InputItem-text">Coin</p>
                  </div>
                  <div className = "ActionCard-spacer"></div>
                  {/*Input the max/min price*/}
                  <div className = "InputItem-flex">
                      <input className = "PriceInput" type="text"></input>
                      <p className = "InputItem-text">
                        {cards[index].action == 'Buy' ? 'Max coin buy price' : 'Min coin sell price'}
                      </p>
                  </div>
                  <div className = "ActionCard-spacer"></div>
                  <div className = "InputItem-flex">
                      <input className = "PriceInput" type="text"></input>
                      <p className = "InputItem-text">Total tx amount</p>
                  </div>
                  <div className = "ActionCard-spacer"></div>
                  <button className="DeleteButton" onClick={() => {removeActionCard(index)}}>
                      <img src={require('./DeleteIcon.png')} className = "DeleteButtonImage" />
                  </button>
              </div>
              ))
            }
          </div>
          <button className = "Add-action" onClick={addCard}>Add order</button>
        </div>
      </header>
    </div>  
  );
}

export default App;
