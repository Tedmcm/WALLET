import subprocess
import json
from constants import *
from dotenv import load_dotenv
import os
from web3 import Web3
from eth_account import Account
from pathlib import Path
from getpass import getpass
load_dotenv()

from bit import PrivateKeyTestnet
from bit.network import NetworkAPI
from bit import wif_to_key

w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))

mnemonic = os.getenv('mnemonic')


def derive_wallets(coin):
    command = f"./derive -g --mnemonic='{mnemonic}' --cols=path,address,privkey,pubkey --format=json --coin='{coin}' --numderive= 2"
    p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    output, err = p.communicate()
    p_status = p.wait()
    keys = json.loads(output)
    return keys

#derive_wallets(ETH)
#print(derive_wallets(ETH))

coins = {
    BTCTEST: derive_wallets(BTCTEST),
    ETH: derive_wallets(ETH)
    
}
print(coins)
INDEX = 0
#print(ETH)

#print(coins[BTCTEST][0][‘privkey’])
#print(coins[ETH][INDEX][‘privkey’])
#print(coins[ETH][0]['privkey'])
#print(w3.eth.blockNumber)
#print(w3.eth.getBalance('0x419D964Bf43A16F79F8A4853E24bDFaD282ecDad'))


def priv_key_to_account(coin, priv_key):
    if coin == ETH:
        return Account.privateKeyToAccount(priv_key)
    elif coin == BTCTEST:
        return PrivateKeyTestnet(priv_key)



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


def send_tx(coin, account, to, amount):
    tx = create_tx(coin, account, to, amount)
    signed_tx = account.sign_transaction(tx)
    if coin == ETH:
        return w3.eth.sendRawTransaction(signed_tx.rawTransaction)

    elif coin == BTCTEST:
        return NetworkAPI.broadcast_tx_testnet(signed_tx)


#BTC ACCOUNT 1
Account_one = priv_key_to_account(BTCTEST, coins[BTCTEST][0]['privkey'])
#ETH ACCOUNT 1

private_key = os.getenv('PRIVATE_KEY')
account_one = Account.from_key(private_key)


#print(Account_one, BTC)
print(coins[BTCTEST][0]['address'])
print(coins[BTCTEST][1]['privkey'])


# insert private key here
key = wif_to_key("cRBQiu7ZZDZHxn7gqRJk8aA3uJgUoYbz8MMC1Hb4Sejgz3GmWyvf")
key2 = wif_to_key("cSWytVTkNrmqGEDFghjpGXhUNm51Khk6Vi6f3Ln73yhzp5i3TY7V")
address_two= coins[BTCTEST][1]['address']

#SEND BTC
send_tx(BTCTEST, Account_one, address_two, 0.002)

#SEND ETH
send_tx(account_one, "7734E2eF879Eb93141f5cE42826aF6d1dBD7c99b", 3)

print(key.get_balance('btc'))
print(key.balance_as('usd'))
#print(key.get_transactions())
#print(key.get_unspents())
print(key2.get_balance('btc'))
print(key2.balance_as('usd'))
#print(key.get_transactions())
#print(key.get_unspents())