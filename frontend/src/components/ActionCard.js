import React, { useState, useEffect } from 'react';  

export default () => {
    const [action, setAction] = useState('Buy');
    const changeAction = event => {
        setAction(event.value);
        console.log(event.value);   
    }

    return <div className = "ActionCard-box">
        <div className = "ActionCard-spacer"></div>
        <div className = "InputItem-flex">
            <select value={action} onChange={e => setAction(e.target.value)} className = "InputItem-dropdown">
                <option value="Buy">Buy</option>
                <option value="Sell">Sell</option>
            </select>
            <p className = "InputItem-text">Action</p>
        </div>
        <div className = "ActionCard-spacer"></div>
        <div className = "InputItem-flex">
            <input className = "PriceInput" type="text"></input>
            <p className = "InputItem-text">{action == 'Buy' ? 'Max coin buy price' : 'Min coin sell price'}</p>
        </div>
        <div className = "ActionCard-spacer"></div>
        {/*TODO: Add state for the coin selected*/}
        <div className = "InputItem-flex">
            <select value={action} onChange={e => setAction(e.target.value)} className = "InputItem-dropdown">
                <option value="Bitcoin">Bitcoin</option>
                <option value="Ethereum">Ethereum</option>
                <option value="Solana">Solana</option>
                <option value="Dogecoin">Dogecoin</option>
            </select>
            <p className = "InputItem-text">Coin</p>
        </div>
        
    </div>
}