import time, os, csv
from dotenv import load_dotenv
load_dotenv()

from functions.get_tocken import get_propertyfinder_token
from functions.listing import get_listing_by_id
from functions.csv_generator import save_to_csv


api_key = os.getenv("API_KEY")
api_secret = os.getenv("API_SECRET")


access_token = get_propertyfinder_token(api_key, api_secret)


# def get_column_values(file_path, column_name):
#     values = []
#     with open(file_path, mode='r', encoding='utf-8') as file:
#         reader = csv.DictReader(file)
#         for row in reader:
#             value = row.get(column_name)
#             if value not in (None, '', 'null', 'NULL'):
#                 values.append(value)
#     return values


# get listings by id and save to csv
# listing_ids = get_column_values("propertyfinder_leads_3.csv", "listing.id")
# for listing_id in listing_ids:
#     access_token = get_propertyfinder_token(api_key, api_secret)
#     print(listing_id)
#     data, pagination = get_listing_by_id(access_token, listing_id)
#     #print(pagination)

#     save_to_csv(data, "listings_from_leads.csv")

