import requests

API_URL = "https://atlas.propertyfinder.com/v1/users"


def get_agent_info(public_profile_id, token):

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
            print('Agent:', data)
            return data.get("data", [])[0] if data.get("data") else None

        else:
            print(f"get user info, error {response.status_code}: {response.text}")
            return None

    except requests.exceptions.RequestException as e:
        print(f"get user info, request error: {e}")
        return None

    except Exception as e:
        print(f"get user info, unexpected error: {e}")
        return None
