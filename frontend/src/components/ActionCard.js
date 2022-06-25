import React, { useState, useEffect } from 'react';  
import Select from 'react-dropdown-select';
import 'font-awesome/css/font-awesome.min.css';

export default () => {
    const coins = [
        { value: 'bitcoin', label: 'BTC' },
        { value: 'ethereum', label: 'ETH' },
        { value: 'solana', label: 'SOL' },
        { value: 'monero', label: 'XMR' },
        { value: 'dogecoin', label: 'DOGE' },   
    ]

    const [action, setAction] = useState('Buy');
    const [coin, setCoin] = useState(null);

    const CoinSelect = () => {
        return <Select
            options = {coins}
            defaultValue = {coin}
            onChange = {e => setCoin(e.target.value)}
            className = "InputItem-dropdown"
        />
    }

    return <div className = "ActionCard-box">
        <div className = "ActionCard-spacer"></div>
        <div className = "InputItem-flex">
            <select 
                value={action} 
                onChange={e => setAction(e.target.value)} 
                className = "InputItem-dropdown">
                <option value="Buy">Buy</option>
                <option value="Sell">Sell</option>
            </select>
            <p className = "InputItem-text">Action</p>
        </div>
        <div className = "ActionCard-spacer"></div>
        <div className = "InputItem-flex">
            <Select
                options = {coins}
                placeholder = 'ETH'
                color = 'white'
                onChange = {(values) => setCoin(values)}
                className = "InputItem-dropdown"
                style = {{width: '100px', 
                borderRadius: '5px',
                border: '1px solid white',}}
                searchable = {false}  
            />
            <p className = "InputItem-text">Coin</p>
        </div>
        <div className = "ActionCard-spacer"></div>
        <div className = "InputItem-flex">
            <input className = "PriceInput" type="text"></input>
            <p className = "InputItem-text">{action == 'Buy' ? 'Max coin buy price' : 'Min coin sell price'}</p>
        </div>
        <div className = "ActionCard-spacer"></div>
        <div className = "InputItem-flex">
            <input className = "PriceInput" type="text"></input>
            <p className = "InputItem-text">Total tx amount</p>
        </div>
        <div className = "ActionCard-spacer"></div>
        <button className="DeleteButton">
            <img src={require('./DeleteIcon.png')} className = "DeleteButtonImage" />
        </button>
    </div>
}