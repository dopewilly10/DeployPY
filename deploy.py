from solcx import compile_standard
from web3 import Web3, AsyncWeb3, AsyncHTTPProvider

from dotenv import load_dotenv
import os
import json

load_dotenv()

with open("./SimpleStorage.sol", "r") as file:
    simple_storage_file = file.read()

# Compile Our Solidity

compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"SimpleStorage.sol": {"content": simple_storage_file}},
        "settings": {
            "outputSelection": {
                "*": {"*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]}
            }
        },
    },
    solc_version="0.6.0",
)


with open("compiled_code.json", "w") as file:
    json.dump(compiled_sol, file)

# get bytecode

bytecode = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"][
    "bytecode"
]["object"]

# get abi

abi = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["abi"]

# for connecting to ganache
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))
chain_id = 5777
my_address = "0x82405c46Ed214bFaA7389b00f359c106966DF7F0"
private_key = os.getenv("PRIVATE_KEY")
print(private_key)
MAX_GAS_ETHER = 0.005

# Create the contract in python
SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)
# get the latest transaction
nonce = w3.eth.get_transaction_count(my_address)
gas_price = int(w3.eth.gas_price)
allowed_gas = int(MAX_GAS_ETHER / gas_price)
print(nonce)

# Build a transaction
# Sign a transaction
# Send a transaction

transaction = SimpleStorage.constructor()._build_transaction(
    {
        "chainId": chain_id,
        "from": my_address,
        "nonce": nonce,
        "gas": allowed_gas,
        "gasPrice": gas_price,
    }
)


signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)
print(signed_txn)

# send signed transaction
# txn_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
