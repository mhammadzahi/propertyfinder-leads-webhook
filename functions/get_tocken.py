import requests, time

def get_propertyfinder_token(api_key: str, api_secret: str):
    time.sleep(1.5)
    
    url = "https://atlas.propertyfinder.com/v1/auth/token"

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    data = {
        "apiKey": api_key,
        "apiSecret": api_secret
    }

    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()  # Raise error if request fails
    return response.json().get("accessToken")

