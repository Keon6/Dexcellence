import '../App.css';
import {useState} from 'react';

function Complex(props) {
  var coins = [
    { value: 'btc', label: 'BTC' },
    { value: 'eth', label: 'ETH' },
    { value: '1inch', label: '1INCH' },
  ]

  const [numCards, setNumCards] = useState(0);
  const [cards, setCards] = useState([
    {
      'index' : numCards,
      'action' : 'Buy',
      'coin' : 'eth',
      'mmp' : 0,
      'ttxa' : 0,
    }
  ]);

  const addCard = i => {
    const newCards = [...cards, {
      'index' : numCards,
      'action' : 'Buy',
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
      updateOrder(start, 'index', start - 1);
      // updateOrder(start, 'action', cards[start-1].action);
      // updateOrder(start, 'coin', cards[start-1].coin);
      // updateOrder(start, 'mmp', cards[start-1].mmp);
      // updateOrder(start, 'ttxa', cards[start-1].ttxa);
    }
    newCards.splice(index, 1);
    for (var i = 0; i < newCards.length; i++) {
      console.log(i + ": " + newCards[i].coin);
    }
    setCards(newCards);
    setNumCards(numCards - 1);
  }

  return (
    <div className="App-main-box">
        <p className="Actions">Make a Complex Order</p>
        <div className = "ActionCardContainer">
        {
            cards.map((order, index) => (
            <div className = "ActionCard-box" key = {index}>
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
                    <select
                    value = {order.coin}
                    placeholder = 'ETH'
                    color = 'white'
                    onChange = {e => updateOrder(index, 'coin', e.target.value)}
                    className = "InputItem-dropdown"
                    >
                    <option value="ETH">ETH</option>
                    <option value="BTC">BTC</option>
                    <option value="1INCH">1INCH</option>
                    </select>
                    <p className = "InputItem-text">Coin</p>
                </div>
                <div className = "ActionCard-spacer"></div>
                {/*Input the max/min price*/}
                <div className = "InputItem-flex">
                    <input className = "PriceInput" type="text" value={order.mmp}
                    onChange={(e) => updateOrder(index, 'mmp', e.target.value)}></input>
                    <p className = "InputItem-text">
                    {cards[index].action == 'Buy' ? 'Max coin buy price' : 'Min coin sell price'}
                    </p>
                </div>
                <div className = "ActionCard-spacer"></div>
                <div className = "InputItem-flex">
                    <input className = "PriceInput" type="text" value={order.ttxa}
                    onChange={(e) => updateOrder(index, 'ttxa', e.target.value)}></input>
                    <p className = "InputItem-text">Total tx amount</p>
                </div>
                <div className = "ActionCard-spacer"></div>
                <button className="DeleteButton" onClick={() => {removeActionCard(index)}}>
                    <img src={require('../DeleteIcon.png')} className = "DeleteButtonImage" />
                </button>
            </div>
            ))
        }
        </div>
        <button className = "Submit" onClick={console.log("Submit")}>Submit</button>
        <button className = "Add-action" onClick={addCard}>Add order</button>
    </div>
  );
}

export default Complex;
