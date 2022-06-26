import '../App.css';
import './swap.css';
import {useState} from 'react';

function Swap(props) {
  var coins = [
    { value: 'btc', label: 'BTC' },
    { value: 'eth', label: 'ETH' },
    { value: 'sol', label: 'SOL' },
  ]

  const [order, setOrder] = useState([
    {
      'index' : 0,
      'action' : 'Buy',
      'coin' : 'eth',
      'mmp' : 0,
      'ttxa' : 0,
    }
  ]);

  const updateOrder = (field, value) => {
    const newOrder = order;
    newOrder[field] = value;
    setOrder(newOrder);
  }

  return (
    <div className="App-main-box">
        <p className="Actions">Make a Swap</p>
        <div className = "Swapbox">
                <div className = "ActionCard-spacer"></div>
                <div className = "ActionCard-spacer"></div>
                {/*Input the action (buy/sell)*/}
                <div className = "InputItem-flex">
                    <select 
                        value={order.action} 
                        onChange={e => updateOrder('action', e.target.value)} 
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
                    onChange = {e => updateOrder('coin', e.target.value)}
                    className = "InputItem-dropdown"
                    >
                    <option value="ETH">ETH</option>
                    <option value="BTC">BTC</option>
                    <option value="SOL">SOL</option>
                    </select>
                    <p className = "InputItem-text">Coin</p>
                </div>
                <div className = "ActionCard-spacer"></div>
                {/*Input the max/min price*/}
                <div className = "InputItem-flex">
                    <input className = "PriceInput" type="text" value={order.mmp}
                    onChange={(e) => updateOrder('mmp', e.target.value)}></input>
                    <p className = "InputItem-text">
                    {order.action == 'Buy' ? 'Max coin buy price' : 'Min coin sell price'}
                    </p>
                </div>
                <div className = "ActionCard-spacer"></div>
                <div className = "InputItem-flex">
                    <input className = "PriceInput" type="text" value={order.ttxa}
                    onChange={(e) => updateOrder('ttxa', e.target.value)}></input>
                    <p className = "InputItem-text">Total tx amount</p>
                </div>
                <div className = "ActionCard-spacer"></div>
            </div>
        <button className = "Submit" onClick={console.log("Submit")}>Submit</button>
    </div>
  );
}

export default Swap;
