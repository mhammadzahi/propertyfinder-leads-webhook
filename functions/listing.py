import requests, time


# TODO: add lcoation filter to the listing id function
# TODO: 

def get_listing_by_id(ACCESS_TOKEN, LISTING_ID):
    time.sleep(1)
    url = "https://atlas.propertyfinder.com/v1/listings"
    params = {
        "filter[ids]": LISTING_ID
    }
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Accept": "application/json"
    }

    response = requests.get(url, headers=headers, params=params)
    print(response.status_code)

    results = response.json().get("results")
    pagination = response.json().get("pagination")

    return results, pagination
