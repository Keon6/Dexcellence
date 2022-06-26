import './App.css';
import './components/Navbar.css'
import Complex from './components/complex';
import Swap from './components/swap';
import './components/portfolio.css'
import {Component, useState, useEffect } from 'react';
import { ethers } from 'ethers';

function Topnav(props) {

  const [errMessage, setErrMessage] = useState(null);
  const [defaultAccount, setDefaultAccount] = useState(null);
  const [userBalance, setUserBalance] = useState(null);

  const openSwap = () => { props.setState('swap') };
  const openComplex = () => { props.setState('complex') };
  const openMore = () => { props.setState('more') };

  const WalletConnectionHandler = () => {
    if(window.ethereum) {
        window.ethereum.request({method: 'eth_requestAccounts'})
        .then(result => {
            AccountHandler(result[0])
            document.getElementById('ButtonConnection').innerText = 'Connected!'
        })
    }
    else
    { 
        errMessage("Please install metamask!");
    }
  }

  const AccountHandler = (newAccount) => {
    setDefaultAccount(newAccount);
    getUserBalc(newAccount);
  }

  const getUserBalc = (address) => {
    window.ethereum.request({method: 'eth_getBalance', params: [address, 'latest']})
    .then(balance => {
        setUserBalance(ethers.utils.formatEther(balance));
    })
    return (
        <div>
        <h4>Balance: {userBalance} ETH</h4>
        </div>
    )
  }

  return (
    <div className="topnav">
      <h3 className="Navbar-header">Dexcellence</h3>
      <ul className='navElements'>
          <li><a href='#Swap' onClick={openSwap}>Swap</a></li>
          <li><a href='#Complex' onClick={openComplex}>Complex Order</a></li>
          <li><a href='#More' onClick={openMore}>More</a></li>  
      </ul>
      <button className="connectButton" id="ButtonConnection" onClick={WalletConnectionHandler}>Connect Wallet</button>
    </div>
  );
}

// Allows us to use state
function Stuff(props) {
  useEffect(() => {
    document.title = "Dexcellence";
  });
  const [state, setState] = useState('swap');
  return (
    <header className="App-header">
      <Topnav setState = {setState}/>
      {state === 'swap' && (<Swap/>)}
      {state === 'complex' && (<Complex/>)}
      <Portfolio />
    </header>
  );
}

function Portfolio(){
  
  return(
    <div className='portfolio-box'>
      <p className="Portfolio-text">My Portfolio</p>
      <div className='portfolio-info'>
        <p className='assets-header'>Assets</p>
        <p className='balance-header'>Balance</p>
        <ul className='assets'>
          <li className='asset-li'>ETH</li>
          <li className='asset-li'>BTC</li>
          <li className='asset-li'>SOL</li>
        </ul>
        <ul className='balances'>
          <li className='asset-li'>10.2</li>
          <li className='asset-li'>0.75</li>
          <li className='asset-li'>20.51</li>
        </ul>
      </div>
    </div>
  )
}

function App(props) {
  return (
    <div className="App">
      <Stuff/>
    </div>
  );
}

export default App;
