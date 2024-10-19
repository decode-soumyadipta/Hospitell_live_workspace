import requests
from requests.auth import HTTPBasicAuth

def upload_to_ipfs(file_path):
    # Infura IPFS API endpoint
    ipfs_url = 'https://ipfs.infura.io:5001/api/v0/add'
    
    # Your Infura Project ID and Project Secret
    project_id = '5f78c1f4513942b48af470c516a08c5c'  # Replace with your Project ID
    project_secret = 'B1k8qpxuNOm9gBCJ9aGxrh6thExpueZEzKnvJW5Jy2LtJ3IK+W8rbg'  # Replace with your Project Secret

    try:
        # Open the file in binary mode
        with open(file_path, 'rb') as file:
            # Make a POST request to upload the file
            response = requests.post(
                ipfs_url,
                files={'file': file},
                auth=HTTPBasicAuth(project_id, project_secret)  # Add authentication
            )

            # Check if the request was successful
            if response.status_code == 200:
                # Return the hash of the uploaded file
                return response.json()['Hash']
            else:
                print(f"Failed to upload file to IPFS: {response.text}")
                return None
    except Exception as e:
        print(f"Error while uploading file to IPFS: {e}")
        return None


