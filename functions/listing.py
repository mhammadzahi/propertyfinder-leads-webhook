import requests, time





def get_listing_by_id(ACCESS_TOKEN, LISTING_ID):
    time.sleep(2)
    url = "https://atlas.propertyfinder.com/v1/listings"
    params = {"filter[ids]": LISTING_ID}
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Accept": "application/json"
    }

    response = requests.get(url, headers=headers, params=params)
    if response.status_code != 200:
        print(f"❌ Listing error: {response.status_code}")
        return None

    data = response.json()
    #print(data)

    listings = data.get("results", [])
    offering_types = data.get("activeCts", {}).get('offeringTypes', [])
    if offering_types:
        print("Offering Types:", offering_types)

    cleaned_listings = []

    for listing in listings:
        # Location enrichment
        loc_id = listing.get("location", {}).get("id")
        location_details = get_location_by_id(ACCESS_TOKEN, loc_id) if loc_id else {}

        # Images: join URLs with '*'
        images = listing.get("media", {}).get("images", [])
        images_str = '*'.join([img.get("original", {}).get("url", "") for img in images])

        # Extract price number only
        price_number = None
        if listing.get("price", {}).get("amounts"):
            for v in listing["price"]["amounts"].values():
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
            "categories": listing.get("category", []),
            "offeringTypes": offering_types,
            "price": price_number,
            "images": images_str,
            "reference": listing.get("reference")
        })

    return cleaned_listings




def get_location_by_id(access_token, location_id):
    time.sleep(2)

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
