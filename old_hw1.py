from create_wallet import generate_algorand_keypair
from complete_transaction import complete_transaction

keypair = generate_algorand_keypair()

# This is where you'd fund the wallet for transactions (https://bank.testnet.algorand.network)
# have this first wallet create asa using asset_example.py

keypair = generate_algorand_keypair()

# This is where you'd fund the wallet for transactions (https://bank.testnet.algorand.network)
#have this second wallet optin to recieving asa

#use transfer_asa.py

complete_transaction(keypair.get("key"), keypair.get("wallet"))
