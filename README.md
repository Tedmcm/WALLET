
# BLOCKCHAIN WALLET

## CREATING A WALLET FOR MY BLOCKCHAIN AND SENDING TRANSACTIONS


For my project I chose the command line tool hd-wallet-derive which can manage billions of addresses across 300 + coins. It supports not only BIP32, BIP39 AND BIP44, but can also support non-standard paths for the most popular wallets out there today. 

I will be starting with 2 working blockchains, a custom Ethereum POA blockchain that I created previously called bzeth and the Bitcoin Testnet. 

## Dependancies
PHP must be installed on your operating system(any version, 5 or 7)
Clone the [hd-wallet-derive tool](https://github.com/dan-da/hd-wallet-derive)
[bit](https://ofek.dev/bit/) Python Bitcoin Library
[web3.py](https://github.com/ethereum/web3.py) Python Ethereum library. 


## Instructions

## HD Derive Wallet Install Guide 

This guide is a step by step process for installing/setting up the [hd-wallet-derive](https://github.com/dan-da/hd-wallet-derive) library used to derive BIP32 addresses and private keys for Bitcoin and other alt coins. 


## HD-WALLET-DERIVE INSTALLATION

Now that the lastest version of PHP is installed on our computers, we can proceed to the installation of the hd-wallet-derive library. 

Execute the following steps:

-Navigate to the [Github Website](https://github.com/dan-da/hd-wallet-derive) for the hd-wallet-derive library and find the installation instructions. 

-Next, open a terminal and execute the following commands. If you are using Windows, you will need to open the git-bash GUI via C:\Program Files\Git\bin\bash.exe directly to enable something called tty mode that makes the terminal more compatible with Unix systems. Once installed, you may move back to using the usual git-bash terminal.


git clone https://github.com/dan-da/hd-wallet-derive
cd hd-wallet-derive
php -r "readfile('https://getcomposer.org/installer');" | php
php -d pcre.jit=0 composer.phar install


-You should now have a folder called hd-wallet-derive containing the PHP library.


# hd-wallet-derive Execution

-Using a command line navigation to your hd-wallet-derive folder


![hd-wallet-derive-folder](/screenshots/hd-wallet-derive-folder.png)


-Then execute the following commands (these are examples from the GitHub website).



./hd-wallet-derive.php -g --key=xprv9tyUQV64JT5qs3RSTJkXCWKMyUgoQp7F3hA1xzG6ZGu6u6Q9VMNjGr67Lctvy5P8oyaYAL9CAWrUE9i6GoNMKUga5biW6Hx4tws2six3b9c


./hd-wallet-derive.php -g --key=xprv9tyUQV64JT5qs3RSTJkXCWKMyUgoQp7F3hA1xzG6ZGu6u6Q9VMNjGr67Lctvy5P8oyaYAL9CAWrUE9i6GoNMKUga5biW6Hx4tws2six3b9c --numderive=3 --preset=bitcoincore --cols=path,address --path-change



![hd-wallet-derive-execute](/screenshots/hd-wallet-derive-execute.png)

I constructed a .py file name wallet.py that which contains functions that enabled me to transact in my bzeth and btc. The following is a break down of the code:

## Function 1
derive_wallet calls out the dictionary of coins with addresses and private keys. 


def derive_wallets(coin):

    command = f"./derive -g --mnemonic='{mnemonic}' --cols=path,address,privkey,pubkey           --format=json --coin='{coin}' --numderive= 2"
    p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    output, err = p.communicate()
    p_status = p.wait()
    keys = json.loads(output)
    return keys

coins = {
    BTCTEST: derive_wallets(BTCTEST),
    ETH: derive_wallets(ETH)
    
}
print(coins)


![function1-coins](/screenshots/function1-coins.png.png)

## Function 2
This function creates the raw, unsigned transaction that contains all metadata needed to tranact. 



def create_tx(coin, account, to, amount):

    if coin == ETH:
        gasEstimate = w3.eth.estimateGas(
            {"from": account.address, "to": to, "value": amount}
        )
        return {
            "from": account.address,
            "to": to,
            "value": amount,
            "gasPrice": w3.eth.gasPrice,
            "gas": gasEstimate,
            "nonce": w3.eth.getTransactionCount(account.address),
            "chainID": w3.eth.chainId
        }
    elif coin == BTCTEST:
        return PrivateKeyTestnet.prepare_transaction(account.address, [(to, amount, BTC)])
        
        
## Function 3
This function calls the previous function, create tx, signs the transaction, then sends it to the designated network. 


def send_tx(coin, account, to, amount):

    tx = create_tx(coin, account, to, amount)
    signed_tx = account.sign_transaction(tx)
    if coin == ETH:
        return w3.eth.sendRawTransaction(signed_tx.rawTransaction)

    elif coin == BTCTEST:
        return NetworkAPI.broadcast_tx_testnet(signed_tx)
        



![BTC_TRANSACTION](/screenshots/BTC_TRANSACTION.png.png)

I ran this function in the wallet.py file: send_tx(BTCTEST, Account_one, address_two, 0.002) to send BTCTEST from one account to another (see folder screen_shots for more imagies).


# ETH Transaction

Local POA Ethereum transaction

-Add one of the ETH addresses to the pre-allocated accounts in your networkname.json.

-Delete the geth folder in each node, then re-initialize using geth --datadir nodeX init networkname.json. This will create a new chain, and will pre-fund the new account.




![RE_INIT_NODE_10](/screenshots/RE_INIT_NODE_10.png)


![RE_INIT_NODE_11](/screenshots/RE_INIT_NODE_11.png)

[Add the following middleware](https://web3py.readthedocs.io/en/stable/middleware.html#geth-style-proof-of-authority) to web3.py to support the PoA algorithm:

from web3.middleware import geth_poa_middleware

w3.middleware_onion.inject(geth_poa_middleware, layer=0)


Due to a bug in web3.py, you will need to send a transaction or two with MyCrypto first, since the w3.eth.generateGasPrice() function does not work with an empty chain. You can use one of the ETH address privkey, or one of the node keystore files.

Send a transaction from the pre-funded address within the wallet to another, then copy the txid into MyCrypto's TX Status, and screenshot the successful transaction like so:


ETH Transaction:

send_tx(account_one, "0x7734E2eF879Eb93141f5cE42826aF6d1dBD7c99b", 3000)