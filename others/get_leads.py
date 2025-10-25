import requests

def get_propertyfinder_leads(access_token: str, page: int, page_size: int):
    url = "https://atlas.propertyfinder.com/v1/leads"

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Bearer {access_token}"
    }
    params = {
        "page": page,
        "pageSize": page_size
        #"createdAtFrom": "2021-04-15T09:00:00+04:00",
        #"createdAtTo": "2021-09-15T09:00:00+04:00"
    }

    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()

    data = response.json().get("data")
    pagination = response.json().get("pagination")
    return data, pagination

