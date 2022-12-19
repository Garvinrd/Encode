import json
import base64
from algosdk.v2client import algod
from algosdk import account, mnemonic
from algosdk.future.transaction import AssetConfigTxn, AssetTransferTxn, AssetFreezeTxn
from algosdk.future.transaction import *


# Shown for demonstration purposes. NEVER reveal secret mnemonics in practice.
# Change these values with your mnemonics
mnemonic1 = "net electric jacket surprise expand exhaust autumn pig dash vendor sense cute loyal rule stay wrap shift account planet clarify until apple oil abandon all"
mnemonic2 = "jeans valve hover uncle soft media struggle gain artwork sting shift oblige pet pink shoulder thrive leisure path differ aunt visa soul focus about shoulder"
mnemonic3 = "recycle hundred scheme minor spirit helmet woman will couch true leisure rapid six fly manage person into height glove business sustain into wasp ability carpet"
# never use mnemonics in production code, replace for demo purposes only

#Fund addresses with algofaucets

# For ease of reference, add account public and private keys to
# an accounts dict.
accounts = {}
counter = 1
for m in [mnemonic1, mnemonic2, mnemonic3]:
    accounts[counter] = {}
    accounts[counter]['pk'] = mnemonic.to_public_key(m)
    accounts[counter]['sk'] = mnemonic.to_private_key(m)
    counter += 1

# Specify your node address and token. This must be updated.
# algod_address = ""  # ADD ADDRESS
# algod_token = ""  # ADD TOKEN

algod_address = "https://testnet-api.algonode.cloud"
algod_client = algod.AlgodClient("", algod_address)

#   Utility function used to print created asset for account and assetid
def print_created_asset(algodclient, account, assetid):    
    # note: if you have an indexer instance available it is easier to just use this
    # response = myindexer.accounts(asset_id = assetid)
    # then use 'account_info['created-assets'][0] to get info on the created asset
    account_info = algodclient.account_info(account)
    idx = 0;
    for my_account_info in account_info['created-assets']:
        scrutinized_asset = account_info['created-assets'][idx]
        idx = idx + 1       
        if (scrutinized_asset['index'] == assetid):
            print("Asset ID: {}".format(scrutinized_asset['index']))
            print(json.dumps(my_account_info['params'], indent=4))
            break

#   Utility function used to print asset holding for account and assetid
def print_asset_holding(algodclient, account, assetid):
    # note: if you have an indexer instance available it is easier to just use this
    # response = myindexer.accounts(asset_id = assetid)
    # then loop thru the accounts returned and match the account you are looking for
    account_info = algodclient.account_info(account)
    idx = 0
    for my_account_info in account_info['assets']:
        scrutinized_asset = account_info['assets'][idx]
        idx = idx + 1        
        if (scrutinized_asset['asset-id'] == assetid):
            print("Asset ID: {}".format(scrutinized_asset['asset-id']))
            print(json.dumps(scrutinized_asset, indent=4))
            break

print("Account 1 address: {}".format(accounts[1]['pk']))
print("Account 2 address: {}".format(accounts[2]['pk']))
print("Account 3 address: {}".format(accounts[3]['pk']))

# your terminal output should look similar to the following
#Account 1 address: TNBHTKWG5NWNGYD4M6XWCGWG7K4OGX3IY23NPCO4WNIXKTWPOX2JC4FQPQ
#Account 2 address: YYNM5XYVNKEMDATPI2EHJ5MV6RAVKIAGOE4BCSOERX4FRCV2X5EHDWHKGE
#Account 3 address: CPKP7V4TH42BFF7Q7T3W3XRKN27OM4ESCKA2M2ECRVXJ2PPZSL35K3SODY

# CREATE ASSET
# Get network params for transactions before every transaction.
params = algod_client.suggested_params()
# comment these two lines if you want to use suggested params
params.fee = 1000
params.flat_fee = True

# Account 1 creates an asset called Big Greg and
# sets Account 2 as the manager, reserve, freeze, and clawback address.
# Asset Creation transaction

txn = AssetConfigTxn(
    sender=accounts[1]['pk'],
    sp=params,
    total=1000,
    default_frozen=False,
    unit_name="Big Greg",
    asset_name="Gr3g",
    manager=accounts[2]['pk'],
    reserve=accounts[2]['pk'],
    freeze=accounts[2]['pk'],
    clawback=accounts[2]['pk'],
    url="https://path/to/my/asset/details", 
    decimals=0)
# Sign with secret key of creator
stxn = txn.sign(accounts[1]['sk'])

# Send the transaction to the network and retrieve the txid.
try:
    txid = algod_client.send_transaction(stxn)
    print("Signed transaction with txID: {}".format(txid))
    # Wait for the transaction to be confirmed
    confirmed_txn = wait_for_confirmation(algod_client, txid, 4)  
    print("TXID: ", txid)
    print("Result confirmed in round: {}".format(confirmed_txn['confirmed-round']))
    print("Transaction information: {}".format(
    json.dumps(confirmed_txn, indent=4)))
# print("Decoded note: {}".format(base64.b64decode(
#     confirmed_txn["txn"]["txn"]["note"]).decode()))
   
except Exception as err:
    print(err)
# Retrieve the asset ID of the newly created asset by first
# ensuring that the creation transaction was confirmed,
# then grabbing the asset id from the transaction.

try:
    # Pull account info for the creator
    # account_info = algod_client.account_info(accounts[1]['pk'])
    # get asset_id from tx
    # Get the new asset's information from the creator account
    ptx = algod_client.pending_transaction_info(txid)
    asset_id = ptx["asset-index"]
    print_created_asset(algod_client, accounts[1]['pk'], asset_id)
    print_asset_holding(algod_client, accounts[1]['pk'], asset_id)
except Exception as e:
    print(e)
# The current manager(Account 2) issues an asset configuration transaction that assigns Account 1 as the new manager.
# Keep reserve, freeze, and clawback address same as before, i.e. account 2
params = algod_client.suggested_params()
# comment these two lines if you want to use suggested params
# params.fee = 1000
# params.flat_fee = True

# asset_id = 149410573;

txn = AssetConfigTxn(
    sender=accounts[2]['pk'],
    sp=params,
    index=asset_id, 
    manager=accounts[1]['pk'],
    reserve=accounts[2]['pk'],
    freeze=accounts[2]['pk'],
    clawback=accounts[2]['pk'])
# sign by the current manager - Account 2
stxn = txn.sign(accounts[2]['sk'])
# txid = algod_client.send_transaction(stxn)
# print(txid)

# Wait for the transaction to be confirmed
# Send the transaction to the network and retrieve the txid.
try:
    txid = algod_client.send_transaction(stxn)
    print("Signed transaction with txID: {}".format(txid))
    # Wait for the transaction to be confirmed
    confirmed_txn = wait_for_confirmation(algod_client, txid, 4) 
    print("TXID: ", txid)
    print("Result confirmed in round: {}".format(confirmed_txn['confirmed-round']))
 
except Exception as err:
    print(err)
# Check asset info to view change in management. manager should now be account 1
print_created_asset(algod_client, accounts[1]['pk'], asset_id)

# OPT-IN

# Check if asset_id is in account 3's asset holdings prior
# to opt-in
params = algod_client.suggested_params()
# comment these two lines if you want to use suggested params
params.fee = 1000
params.flat_fee = True

account_info = algod_client.account_info(accounts[3]['pk'])
holding = None
idx = 0
for my_account_info in account_info['assets']:
    scrutinized_asset = account_info['assets'][idx]
    idx = idx + 1    
    if (scrutinized_asset['asset-id'] == asset_id):
        holding = True
        break

if not holding:

    # Use the AssetTransferTxn class to transfer assets and opt-in
    txn = AssetTransferTxn(
        sender=accounts[3]['pk'],
        sp=params,
        receiver=accounts[3]["pk"],
        amt=0,
        index=asset_id)
    stxn = txn.sign(accounts[3]['sk'])
    # Send the transaction to the network and retrieve the txid.
    try:
        txid = algod_client.send_transaction(stxn)
        print("Signed transaction with txID: {}".format(txid))
        # Wait for the transaction to be confirmed
        confirmed_txn = wait_for_confirmation(algod_client, txid, 4) 
        print("TXID: ", txid)
        print("Result confirmed in round: {}".format(confirmed_txn['confirmed-round']))
 
    except Exception as err:
        print(err)
    # Now check the asset holding for that account.
    # This should now show a holding with a balance of 0.
    print_asset_holding(algod_client, accounts[3]['pk'], asset_id)

# TRANSFER ASSET

# transfer asset of 10 from account 1 to account 3
params = algod_client.suggested_params()
# comment these two lines if you want to use suggested params
params.fee = 1000
params.flat_fee = True
txn = AssetTransferTxn(
    sender=accounts[1]['pk'],
    sp=params,
    receiver=accounts[3]["pk"],
    amt=10,
    index=asset_id)
stxn = txn.sign(accounts[1]['sk'])
# Send the transaction to the network and retrieve the txid.
try:
    txid = algod_client.send_transaction(stxn)
    print("Signed transaction with txID: {}".format(txid))
    # Wait for the transaction to be confirmed
    confirmed_txn = wait_for_confirmation(algod_client, txid, 4) 
    print("TXID: ", txid)
    print("Result confirmed in round: {}".format(confirmed_txn['confirmed-round']))

except Exception as err:
    print(err)
# The balance should now be 10.
print_asset_holding(algod_client, accounts[3]['pk'], asset_id)   

#         garvinrd@Richards-Air AlgoEncode % python3 hw1.py
# Account 1 address: TNBHTKWG5NWNGYD4M6XWCGWG7K4OGX3IY23NPCO4WNIXKTWPOX2JC4FQPQ
# Account 2 address: YYNM5XYVNKEMDATPI2EHJ5MV6RAVKIAGOE4BCSOERX4FRCV2X5EHDWHKGE
# Account 3 address: CPKP7V4TH42BFF7Q7T3W3XRKN27OM4ESCKA2M2ECRVXJ2PPZSL35K3SODY
# Signed transaction with txID: NJ2OJD4IZMRGFABJHGEBQARENAIYFDIIFFXQPSDRAOSOXFR5C6AQ
# TXID:  NJ2OJD4IZMRGFABJHGEBQARENAIYFDIIFFXQPSDRAOSOXFR5C6AQ
# Result confirmed in round: 26375855
# Transaction information: {
#     "asset-index": 149412154,
#     "confirmed-round": 26375855,
#     "pool-error": "",
#     "txn": {
#         "sig": "hxCEPiQxjyh7Arcyrl2BW59DadTS9IyNN/LgDDKgiRK6iiFlrzvq5OGWh5EFr3WB9mqTWPph106tIEGWmM04Bw==",
#         "txn": {
#             "apar": {
#                 "an": "Gr3g",
#                 "au": "https://path/to/my/asset/details",
#                 "c": "YYNM5XYVNKEMDATPI2EHJ5MV6RAVKIAGOE4BCSOERX4FRCV2X5EHDWHKGE",
#                 "f": "YYNM5XYVNKEMDATPI2EHJ5MV6RAVKIAGOE4BCSOERX4FRCV2X5EHDWHKGE",
#                 "m": "YYNM5XYVNKEMDATPI2EHJ5MV6RAVKIAGOE4BCSOERX4FRCV2X5EHDWHKGE",
#                 "r": "YYNM5XYVNKEMDATPI2EHJ5MV6RAVKIAGOE4BCSOERX4FRCV2X5EHDWHKGE",
#                 "t": 1000,
#                 "un": "Big Greg"
#             },
#             "fee": 1000,
#             "fv": 26375853,
#             "gen": "testnet-v1.0",
#             "gh": "SGO1GKSzyE7IEPItTxCByw9x8FmnrCDexi9/cOUJOiI=",
#             "lv": 26376853,
#             "snd": "TNBHTKWG5NWNGYD4M6XWCGWG7K4OGX3IY23NPCO4WNIXKTWPOX2JC4FQPQ",
#             "type": "acfg"
#         }
#     }
# }
# Asset ID: 149412154
# {
#     "clawback": "YYNM5XYVNKEMDATPI2EHJ5MV6RAVKIAGOE4BCSOERX4FRCV2X5EHDWHKGE",
#     "creator": "TNBHTKWG5NWNGYD4M6XWCGWG7K4OGX3IY23NPCO4WNIXKTWPOX2JC4FQPQ",
#     "decimals": 0,
#     "default-frozen": false,
#     "freeze": "YYNM5XYVNKEMDATPI2EHJ5MV6RAVKIAGOE4BCSOERX4FRCV2X5EHDWHKGE",
#     "manager": "YYNM5XYVNKEMDATPI2EHJ5MV6RAVKIAGOE4BCSOERX4FRCV2X5EHDWHKGE",
#     "name": "Gr3g",
#     "name-b64": "R3IzZw==",
#     "reserve": "YYNM5XYVNKEMDATPI2EHJ5MV6RAVKIAGOE4BCSOERX4FRCV2X5EHDWHKGE",
#     "total": 1000,
#     "unit-name": "Big Greg",
#     "unit-name-b64": "QmlnIEdyZWc=",
#     "url": "https://path/to/my/asset/details",
#     "url-b64": "aHR0cHM6Ly9wYXRoL3RvL215L2Fzc2V0L2RldGFpbHM="
# }
# Asset ID: 149412154
# {
#     "amount": 1000,
#     "asset-id": 149412154,
#     "is-frozen": false
# }
# Signed transaction with txID: OOBLTEXHT3UKXJSBQLF3JUYCMQ56J4XREEOIYCYFYD42ILE5GNCA
# TXID:  OOBLTEXHT3UKXJSBQLF3JUYCMQ56J4XREEOIYCYFYD42ILE5GNCA
# Result confirmed in round: 26375857
# Asset ID: 149412154
# {
#     "clawback": "YYNM5XYVNKEMDATPI2EHJ5MV6RAVKIAGOE4BCSOERX4FRCV2X5EHDWHKGE",
#     "creator": "TNBHTKWG5NWNGYD4M6XWCGWG7K4OGX3IY23NPCO4WNIXKTWPOX2JC4FQPQ",
#     "decimals": 0,
#     "default-frozen": false,
#     "freeze": "YYNM5XYVNKEMDATPI2EHJ5MV6RAVKIAGOE4BCSOERX4FRCV2X5EHDWHKGE",
#     "manager": "TNBHTKWG5NWNGYD4M6XWCGWG7K4OGX3IY23NPCO4WNIXKTWPOX2JC4FQPQ",
#     "name": "Gr3g",
#     "name-b64": "R3IzZw==",
#     "reserve": "YYNM5XYVNKEMDATPI2EHJ5MV6RAVKIAGOE4BCSOERX4FRCV2X5EHDWHKGE",
#     "total": 1000,
#     "unit-name": "Big Greg",
#     "unit-name-b64": "QmlnIEdyZWc=",
#     "url": "https://path/to/my/asset/details",
#     "url-b64": "aHR0cHM6Ly9wYXRoL3RvL215L2Fzc2V0L2RldGFpbHM="
# }
# Signed transaction with txID: UYTY2V7636LY7MFUACSJDEQGR5UEP7MMMTFPNKU6X7K5FNPADFUA
# TXID:  UYTY2V7636LY7MFUACSJDEQGR5UEP7MMMTFPNKU6X7K5FNPADFUA
# Result confirmed in round: 26375859
# Asset ID: 149412154
# {
#     "amount": 0,
#     "asset-id": 149412154,
#     "is-frozen": false
# }
# Signed transaction with txID: FRAVPXQBTXBOFSNZWZV45HLEDUZYHLIZJLVMEWBP55UDFTSTCWHA
# TXID:  FRAVPXQBTXBOFSNZWZV45HLEDUZYHLIZJLVMEWBP55UDFTSTCWHA
# Result confirmed in round: 26375861
# Asset ID: 149412154
# {
#     "amount": 10,
#     "asset-id": 149412154,
#     "is-frozen": false