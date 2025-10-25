import requests, time, os, csv
from dotenv import load_dotenv
from functions.get_tocken import get_propertyfinder_token
from functions.get_leads import get_propertyfinder_leads
from functions.csv_generator import save_to_csv
from functions.listing import get_listing_by_id
from functions.s3_downloader import download_all_from_csv

from functions.webhook import subscribe_to_webhook


load_dotenv()

api_key = os.getenv("API_KEY")
api_secret = os.getenv("API_SECRET")


access_token = get_propertyfinder_token(api_key, api_secret)
print(access_token)


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


# get leads from property finder and save to csv
# for i in range(183, 201):
    # access_token = get_propertyfinder_token(api_key, api_secret)
    # time.sleep(7)
    #data, pagination = get_propertyfinder_leads(access_token, page=i, page_size=50) # 2

    
    # print("data:", data)
    # print("pagination:", pagination)

    # save_to_csv(data, "propertyfinder_leads_3.csv")
    # time.sleep(5)

    # download_all_from_csv("propertyfinder_leads_3.csv", url_column="call.recordFile", save_dir="recordings", force_download=False)

