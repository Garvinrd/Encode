from algosdk.v2client import algod

#initalize client
algod_address = "https://testnet-api.algonode.cloud"
algod_client = algod.AlgodClient("", algod_address)

asset_creator_address = "PZ5ZLWQSCZKQ2JYO2AW5I3LUGHHF7XDHLH7RSICPMKR74GWJUVBE4QUP74"
passphrase = "shine buzz broken awkward easily final debris tank wire demise hill grace gauge seminar invest erosion anger real jeans gallery retreat swift trap absorb include"

# define the smart contract
smart_contract = f"""
txn ENB_minimum 1000
txn Yes_vote 0
txn No_vote 0
txn Abstain_vote 0

int ENB
int Choice
int ENB_vote

# check if voter holds enough ENB
int ENB_check
ENB_check = balance(txn.sender)

txn ENB_check_result
ENB_check_result = (ENB_check >= ENB_minimum)

# check if vote choice is valid
int choice_check
choice_check = (Choice == 1 || Choice == 2 || Choice == 3)

txn choice_check_result
choice_check_result = (ENB_check_result && choice_check)

# increase vote count
if choice_check_result
    int voter_ENB
    voter_ENB = balance(txn.sender)
    ENB_vote = voter_ENB
    if (Choice == 1)
        Yes_vote += voter_ENB
    else if (Choice == 2)
        No_vote += voter_ENB
    else if (Choice == 3)
        Abstain_vote += voter_ENB
endif

# decrease vote count
if (Choice == 4)
    int voter_ENB
    voter_ENB = balance(txn.sender)
    ENB_vote = voter_ENB
    if (Choice == 1)
        Yes_vote -= voter_ENB
    else if (Choice == 2)
        No_vote -= voter_ENB
    else if (Choice == 3)
        Abstain_vote -= voter_ENB
endif
"""

# compile the smart contract
smart_contract = pyteal.compile(smart_contract)

# deploy the smart contract
txid = algod_client.deploy_contract(smart_contract, "YOUR_ALGOD_ADDRESS")

print("Smart contract deployed successfully with txid: ", txid)
