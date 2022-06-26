import React, {useState} from 'react'
import { ethers } from 'ethers';
import './Navbar.css'
export default () => {
    
const [errMessage, setErrMessage] = useState(null);
    const [defaultAccount, setDefaultAccount] = useState(null);
    const [userBalance, setUserBalance] = useState(null);

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
        <div class="topnav">
            <h3 className="Navbar-header">Dexcellence</h3>
            <ul className='navElements'>
                <li><a href="#Swap">Swap</a></li>
                <li><a href="#Complex">Complex Order</a></li>
                            <li><a href="#More">More</a></li>  
            </ul>
            <button className="connectButton" id="ButtonConnection" onClick={WalletConnectionHandler}>Connect Wallet</button>
            </div>
    )

}