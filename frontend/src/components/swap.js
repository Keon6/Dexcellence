import '../App.css';
import './swap.css';
import {useState} from 'react';

function Swap(props) {
  var coins = [
    { value: 'btc', label: 'BTC' },
    { value: 'eth', label: 'ETH' },
    { value: 'sol', label: 'SOL' },
  ]

  const [action, setAction] = useState('Buy');
  const [coin, setCoin] = useState('ETH');
  const [mmp, setMmp] = useState(0);
  const [ttxa, setTtxa] = useState(0);

  return (
    <div className="Swap-main-box">
        <p className="Actions">Make a Swap</p>
        <div className = "Swapbox">
                {/*Input the action (buy/sell)*/}
                <div className = "SwapInputItem-flex SwapAction">
                    <select 
                        value={action} 
                        onChange={e => setAction(e.target.value)} 
                        className = "SwapInputItem-dropdown">
                        <option value='Buy'>Buy</option>
                        <option value='Sell'>Sell</option>
                    </select>
                    <p className = "SwapInputItem-text">Action</p>
                </div>
                {/*Input the coin*/}
                <div className = "SwapInputItem-flex SwapCoin">
                    <select
                    value = {coin}
                    placeholder = 'ETH'
                    color = 'white'
                    onChange = {e => setCoin(e.target.value)}
                    className = "SwapInputItem-dropdown"
                    >
                    <option value="ETH">ETH</option>
                    <option value="BTC">BTC</option>
                    <option value="SOL">SOL</option>
                    </select>
                    <p className = "SwapInputItem-text">Coin</p>
                </div>
                {/*Input the max/min price*/}
                <div className = "SwapInputItem-flex SwapMmp">
                    <input className = "SwapPriceInput" type="text" value={mmp}
                    onChange={(e) => setMmp(e.target.value)}></input>
                    <p className = "SwapInputItem-text">
                    {action == 'Buy' ? 'Max coin buy price' : 'Min coin sell price' }
                    </p>
                </div>
                <div className = "SwapInputItem-flex SwapTtxa">
                    <input className = "SwapPriceInput" type="text" value={ttxa}
                    onChange={(e) => setTtxa(e.target.value)}></input>
                    <p className = "SwapInputItem-text">Total tx amount</p>
                </div>
                <button className = "SwapSubmit" onClick={()=>console.log("Submit")}>Submit</button>
            </div>
    </div>
  );
}

export default Swap;
