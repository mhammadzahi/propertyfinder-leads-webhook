import os

from dotenv import load_dotenv
load_dotenv()


from functions.get_tocken import get_propertyfinder_token
from functions.listing import get_listing_by_id

from functions.csv_reader import get_column_values
from functions.csv_generator import save_to_csv


api_key = os.getenv("API_KEY")
api_secret = os.getenv("API_SECRET")



listing_ids = get_column_values("propertyfinder_leads_3.csv", "listing.id")

for listing_id in listing_ids:

    access_token = get_propertyfinder_token(api_key, api_secret)
    data = get_listing_by_id(access_token, listing_id.strip())

    save_to_csv(data, "listings_with_location_and_agent_from_leads.csv")

