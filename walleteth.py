import subprocess
import json
from constants import *
from dotenv import load_dotenv
import os
from web3 import Web3
from eth_account import Account
from bit import wif_to_key
load_dotenv()
from bit import PrivateKeyTestnet
from bit.network import NetworkAPI
from web3.auto.gethdev import w3
from web3.middleware import geth_poa_middleware



w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
print(w3.eth.blockNumber)
print(w3.eth.getBalance("0x7734E2eF879Eb93141f5cE42826aF6d1dBD7c99b"))
private_key = os.getenv('PRIVATE_KEY')
print(private_key)

account_one = Account.from_key(private_key)
print(account_one.address)

#with open(
#   Path(
#       "UTC--2020-10-24T17-11-29.986388000Z--01b2f4dd29d0ffd56784fdbe4954916ff5805b9c"
#    )
#) as keyfile:
#   encrypted_key = keyfile.read()
#    private_key = w3.eth.account.decrypt(
#        encrypted_key, getpass("Enter keystore password: ")
#    )
#    account_two = Account.from_key(private_key)



def create_raw_tx(account, recipient, amount):
    gasEstimate = w3.eth.estimateGas(
        {"from": account.address, "to": recipient, "value": amount}
    )
    return {
        "from": account.address,
        "to": recipient,
        "value": amount,
        "gasPrice": w3.eth.gasPrice,
        "gas": gasEstimate,
        "nonce": w3.eth.getTransactionCount(account.address),
    }

def send_tx(account, recipient, amount):
    tx = create_raw_tx(account, recipient, amount)
    signed_tx = account.sign_transaction(tx)
    result = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
    print(result.hex())
    return result.hex()

print(send_tx(account_one, "0x7734E2eF879Eb93141f5cE42826aF6d1dBD7c99b", 100)) #account_one is sender, # is Receipt acct/who your sending to

#This prints if transaction worked to keystore account (above with utc code part)
# when you run this part in terminal you will be asked for keystore password lamborghini2020! in terminal)
# you will see in terminal the account address from you mycrypto that matches
#print(account_two.adress)


#THE FOLLOWING IS JUST PRINT STATEMENT LIKE RECIEPT TO SHOW TRANSACTION ON NODE/CHAIN.(ATTRIBUTE DICTIONARY YOU WILL SEE IN TERMINAL RUNNING NODE1)
# the follwing number is number you get from terminal that shows transaction in your running node! it has hash # and recepient #!
print(w3.eth.getTransactionReceipt("0xbd5977b98424b69d5f957bbd2d7f533dca44d1d8686107d7664b619628f8bcc4"))