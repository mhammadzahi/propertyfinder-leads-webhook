import requests

API_URL = "https://atlas.propertyfinder.com/v1/users"


def get_user_info(public_profile_id, token):
    """
    Fetches user info from Propertyfinder Atlas API using the publicProfile ID (GET method).
    
    Args:
        public_profile_id (int): The publicProfile ID of the lead.
        
    Returns:
        dict: User info from the API response or None if not found/error.
    """
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    params = {
        "publicProfileId": str(public_profile_id)
    }
    
    try:
        response = requests.get(API_URL, headers=headers, params=params)
        if response.status_code == 200:
            data = response.json()
            return data.get("data", [])[0] if data.get("data") else None
        else:
            print(f"Error {response.status_code}: {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        return None



# Example usage with your lead data
# lead = {
#     'id': 'lead-created-24680649',
#     'payload': {
#         'publicProfile': {'id': 207553}
#     }
# }

# user_info = get_user_info(lead['payload']['publicProfile']['id'])
# print(user_info)
