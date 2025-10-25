import requests, time




def get_listing_by_id(ACCESS_TOKEN, LISTING_ID, categories=None, offeringTypes=None):
    time.sleep(1)

    if categories is None:
        categories = ["residential"]
    if offeringTypes is None:
        offeringTypes = ["rent"]

    url = "https://atlas.propertyfinder.com/v1/listings"
    params = {
        "filter[ids]": LISTING_ID,
        "categories": categories,
        "offeringTypes": offeringTypes,
        "page": 1,
        "perPage": 10
    }
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Accept": "application/json"
    }

    response = requests.get(url, headers=headers, params=params)
    if response.status_code != 200:
        print(f"❌ Listing error: {response.status_code}")
        return None

    data = response.json()
    listings = data.get("results", [])

    cleaned_listings = []

    for listing in listings:
        # Enrich location
        loc_id = listing.get("location", {}).get("id")
        location_details = get_location_by_id(ACCESS_TOKEN, loc_id) if loc_id else {}

        # Join all image URLs into a single string separated by '*'
        images = listing.get("media", {}).get("images", [])
        images_str = '*'.join([img.get("original", {}).get("url", "") for img in images])

        # Extract only the number from price
        price_number = None
        if listing.get("price", {}).get("amounts"):
            amounts = listing["price"]["amounts"]
            for v in amounts.values():
                if v:
                    price_number = v
                    break

        cleaned_listings.append({
            "location_id": location_details.get("id"),
            "name": location_details.get("name"),
            "city_name": location_details.get("city_name"),
            "community_name": location_details.get("community_name"),
            "sub_community_name": location_details.get("sub_community_name"),
            "bedrooms": listing.get("bedrooms"),
            "categories": categories,
            "offeringTypes": offeringTypes,
            "price": price_number,
            "images": images_str,
            "reference": listing.get("reference")
        })

    return {
        "results": cleaned_listings
    }




def get_location_by_id(access_token, location_id):
    time.sleep(1)
    
    url = "https://atlas.propertyfinder.com/v1/locations"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/json"
    }
    params = {"filter[id]": location_id, "perPage": 1}
    response = requests.get(url, headers=headers, params=params)
    if response.status_code != 200:
        return None
    data = response.json().get("data", [])
    if not data:
        return None

    loc = data[0]
    tree = loc.get("tree", [])
    city_name = community_name = sub_community_name = None
    for node in tree:
        t = node.get("type")
        if t == "CITY":
            city_name = node.get("name")
        elif t == "COMMUNITY":
            community_name = node.get("name")
        elif t == "SUBCOMMUNITY":
            sub_community_name = node.get("name")

    return {
        "id": loc.get("id"),
        "name": loc.get("name"),
        "city_name": city_name,
        "community_name": community_name,
        "sub_community_name": sub_community_name
    }


