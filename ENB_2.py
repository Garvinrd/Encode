from algosdk.v2client import algod
from algosdk.future.transaction import AssetConfigTxn, wait_for_confirmation
from algosdk.mnemonic import to_private_key
import json
import requests

algod_address = "https://testnet-api.algonode.cloud"
algod_client = algod.AlgodClient("", algod_address)

asset_creator_address = "PZ5ZLWQSCZKQ2JYO2AW5I3LUGHHF7XDHLH7RSICPMKR74GWJUVBE4QUP74"
passphrase = "shine buzz broken awkward easily final debris tank wire demise hill grace gauge seminar invest erosion anger real jeans gallery retreat swift trap absorb include"

# define the asset parameters
params = {
    "creator": asset_creator_address,
    "name": "ENB",
    "unitname": "ENB",
    "total": 1000000000,
    "decimals": 0,
    "default_frozen": False,
    "manager": asset_creator_address,
    "reserve": asset_creator_address,
    "freeze": asset_creator_address,
    "clawback": asset_creator_address,
    "url": "https://path/to/my/asset/details",
    "metadata_hash": "",
    "decimals": 0
}

# create the asset
response = requests.post("https://testnet-api.algonode.cloud", json=params, headers={'Content-type': 'application/json'})

#get the ASA ID
asa_id = response.json()["index"]

# write the smart contract in TEAL
smart_contract = f"""
txn AssetID {asa_id}
txn AssetENB "ENB"
"""

# encode the smart contract
smart_contract_encoded = bytes(smart_contract, 'ascii').hex()

# define the transaction parameters
tx_params = {
    "from": asset_creator_address,
    "note": smart_contract_encoded,
    "fee": 1000,
    "flat_fee": True
}

# sign the transaction
response = requests.post("https://api.algoexplorer.io/v1/accounts/transact", json=tx_params, headers={'Content-type': 'application/json'})

# get the transaction ID
tx_id = response.json()["txId"]

print("Smart contract deployed successfully with txid: ", tx_id)
