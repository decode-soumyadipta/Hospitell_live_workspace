import json
from web3 import Web3
import os
from dotenv import load_dotenv

# Load environment variables (for sensitive information like private keys, contract address, etc.)
load_dotenv()

# Kaleido RPC URL for Ethereum node
KALEIDO_RPC_URL = os.getenv("KALEIDO_RPC_URL")  # Make sure this is in your .env file
CONTRACT_ADDRESS = os.getenv("CONTRACT_ADDRESS")  # Smart contract address on Kaleido
PRIVATE_KEY = os.getenv("PRIVATE_KEY")  # Your private key (used to sign transactions)
USER_ADDRESS = os.getenv("USER_ADDRESS")  # Your Ethereum wallet address (public)

# Connect to Kaleido blockchain using Web3
w3 = Web3(Web3.HTTPProvider(KALEIDO_RPC_URL))

# Check if the connection is successful
if not w3.is_connected():
    raise ConnectionError("Unable to connect to Kaleido. Please check your RPC URL and internet connection.")

# Load the contract ABI (assuming you have already deployed the contract)
with open('utils/ABI.json', 'r') as abi_file:
    contract_abi = json.load(abi_file)

# Convert the contract address to checksum format
contract_address = Web3.to_checksum_address(CONTRACT_ADDRESS)

# Initialize the contract
contract = w3.eth.contract(address=contract_address, abi=contract_abi)

def store_data_on_blockchain(prescription_hash, test_results_hash):
    """
    Store prescription and test results hash on the Kaleido blockchain.
    
    Arguments:
    - prescription_hash: The IPFS hash of the prescription file.
    - test_results_hash: The IPFS hash of the test results file.
    
    Returns:
    - Transaction hash as a string if successful, or None if there was an error.
    """
    try:
        # Convert your user address to checksum format
        user_address = Web3.to_checksum_address(USER_ADDRESS)

        # Get the latest nonce for your account (needed for transaction)
        nonce = w3.eth.getTransactionCount(user_address)

        # Build the transaction to call the smart contract's storeMedicalData function
        txn = contract.functions.storeMedicalData(prescription_hash, test_results_hash).buildTransaction({
            'chainId': 1337,  # Chain ID for Kaleido private networks (1337 is often used for private chains)
            'gas': 2000000,   # Gas limit for the transaction
            'gasPrice': w3.toWei('20', 'gwei'),  # Gas price in Gwei
            'nonce': nonce,   # Nonce value for transaction uniqueness
        })

        # Sign the transaction with your private key
        signed_txn = w3.eth.account.signTransaction(txn, PRIVATE_KEY)

        # Send the signed transaction to the blockchain
        tx_hash = w3.eth.sendRawTransaction(signed_txn.rawTransaction)

        # Print or return the transaction hash (optional logging for debugging)
        print(f"Transaction successful with hash: {tx_hash.hex()}")
        return tx_hash.hex()

    except Exception as e:
        print(f"An error occurred while storing data on the blockchain: {e}")
        return None
