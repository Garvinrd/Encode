from algosdk import account, mnemonic

def generate_algorand_keypair():
    private_key, address = account.generate_account()
    print("My address: {}".format(address))
    print("My private key: {}".format(private_key))
    print("My passphrase {}".format(mnemonic.from_private_key(private_key)))
    return {"key":private_key, "wallet":address}

# Write down the address, private key, and the passphrase for later usage
generate_algorand_keypair()