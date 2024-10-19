import json
from web3 import Web3

# Connect to Sepolia Testnet via Infura
w3 = Web3(Web3.HTTPProvider('https://sepolia.infura.io/v3/5f78c1f4513942b48af470c516a08c5c'))

# Load contract ABI and address
with open('utils/ABI.json', 'r') as abi_file:
    contract_abi = json.load(abi_file)

contract_address = '0x7df8ff2011e33349dc49cef578e3627610e5f706'  # Make sure this is your Sepolia deployed contract address

# Convert the contract address to a checksum address
contract_address = Web3.to_checksum_address(contract_address)
contract = w3.eth.contract(address=contract_address, abi=contract_abi)


def store_data_on_blockchain(user_address, prescription_hash, test_results_hash, private_key):
    try:
        # Convert user_address to checksum address
        user_address = Web3.to_checksum_address(user_address)

        # Get the latest nonce for the user's address
        nonce = w3.eth.getTransactionCount(user_address)

        # Create the transaction
        txn = contract.functions.storeMedicalData(prescription_hash, test_results_hash).buildTransaction({
            'chainId': 11155111,  # Sepolia testnet chain id
            'gas': 2000000,
            'gasPrice': w3.toWei('50', 'gwei'),
            'nonce': nonce,
        })

        # Sign the transaction
        signed_txn = w3.eth.account.signTransaction(txn, private_key)

        # Send the transaction
        tx_hash = w3.eth.sendRawTransaction(signed_txn.rawTransaction)

        # Return the transaction hash in hex format
        return tx_hash.hex()

    except Exception as e:
        print(f"An error occurred while storing data on the blockchain: {e}")
        return None

# Example of how to call the function
# Replace these values with actual data when you're ready
user_address = '0xYourUserAddressHere'
prescription_hash = 'QmYourPrescriptionHashFromIPFS'
test_results_hash = 'QmYourTestResultsHashFromIPFS'
private_key = '0xYourPrivateKeyHere'

# Store the data on the blockchain
tx_hash = store_data_on_blockchain(user_address, prescription_hash, test_results_hash, private_key)

print(f"Transaction successful with hash: {tx_hash}")
