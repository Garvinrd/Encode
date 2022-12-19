import json
import base64
from algosdk import constants
from algosdk.v2client import algod
from algosdk.future import transaction

def complete_transaction(private_key, my_address):
    print("completing transaction")
    print(private_key)
    print(my_address)
    algod_address = "https://testnet-api.algonode.cloud"
    algod_client = algod.AlgodClient("", algod_address)

    print("My address: {}".format(my_address))
    account_info = algod_client.account_info(my_address)
    account_info = algod_client.account_info(my_address)
    print("Account balance: {} microAlgos".format(account_info.get('amount')))

    # build transaction
    params = algod_client.suggested_params()
    
    # comment out the next two (2) lines to use suggested fees
    params.flat_fee = constants.MIN_TXN_FEE 
    params.fee = 1000
    receiver = "HZ57J3K46JIJXILONBBZOHX6BKPXEM2VVXNRFSUED6DKFD5ZD24PMJ3MVA"
    amount = 100000
    note = "Hello World".encode()

    unsigned_txn = transaction.PaymentTxn(my_address, params, receiver, amount, None, note)


    # sign transaction
    signed_txn = unsigned_txn.sign(private_key)

    # submit transaction
    txid = algod_client.send_transaction(signed_txn)
    print("Signed transaction with txID: {}".format(txid))
    #- - - -
    # wait for confirmation 
    try:
        confirmed_txn = transaction.wait_for_confirmation(algod_client, txid, 4)  
        print("Transaction information: {}".format(
        json.dumps(confirmed_txn, indent=4)))
        print("Decoded note: {}".format(base64.b64decode(
        confirmed_txn["txn"]["txn"]["note"]).decode()))
        print("Starting Account balance: {} microAlgos".format(account_info.get('amount')) )
        print("Amount transfered: {} microAlgos".format(amount) )    
        print("Fee: {} microAlgos".format(params.fee) ) 

        account_info = algod_client.account_info(my_address)
        print("Final Account balance: {} microAlgos".format(account_info.get('amount')) + "\n")
        return True
    except Exception as err:
        print(err)
        return False
    