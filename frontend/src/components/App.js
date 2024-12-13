import React from 'react';
import logo from '../assets/logo.png';
import { Link } from 'react-router-dom';
import { useEffect, useState } from 'react';
import {API_BASE_URL} from '../config';


function App() {
  const [walletInfo, setWalletInfo] = useState({});

  useEffect(() => {
    fetch(`${API_BASE_URL}/wallet/info`)
    .then(response => response.json())
    .then(json => setWalletInfo(json));
  }, []);

  const {address, balance} = walletInfo;

  return (
    <div className="App">
      <img className='logo' src={logo} alt = 'application-logo'/>
      <h3>Welcome to BlockSync Ledger</h3>
      <br/>
      <Link to='/blockchain'>Blockchain</Link>
      <Link to='/conduct-transaction'>Conduct a Transaction</Link>
      <Link to='/transaction-pool'>Transaction Pool</Link>
      <div className='WalletInfo'>
        <div>Address: {address}</div>
        <div>Balance: {balance}</div>
      </div>
    </div>
  );
}

export default App;
