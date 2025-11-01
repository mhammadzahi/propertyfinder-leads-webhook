import os, json

from functions.get_tocken import get_propertyfinder_token
from functions.listing import get_listing_by_id
from functions.leads import get_leads

from functions.csv_reader import get_column_values
from functions.csv_generator import save_to_csv, generate_listing_by_id

from functions.s3_downloader import download_all_from_csv
from functions.s3_uploader import main_upload

from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv("API_KEY")
api_secret = os.getenv("API_SECRET")



main_upload("recordings")



# 2 generate listing with locations and mapper csv files
# listing_ids = get_column_values("propertyfinder_leads_10K__2__.csv", "listing.id")
# i = 2
# for listing_id in listing_ids:
#     access_token = get_propertyfinder_token(api_key, api_secret)
#     data = get_listing_by_id(access_token, listing_id.strip())
#     save_to_csv(data, "listings_with_location_10K__2__.csv")
#     if data:
#         generate_listing_by_id("listing_by_id_10K__2__.csv", listing_id, i, json.dumps(data))# Natalia Mapping
#         i += 1

#     else:
#         print(f"No Data for listing id: {listing_id}")




# 1 Pull Leads 10K
# lead_csv_file = "propertyfinder_leads_10K__2__.csv"
# for j in range(1, 201):
#     access_token = get_propertyfinder_token(api_key, api_secret)
#     data, pagination = get_leads(access_token, j, 50)

#     save_to_csv(data, lead_csv_file)
#     download_all_from_csv(csv_file=lead_csv_file, url_column="call.recordFile", save_dir="recordings", force_download=False)

#     print(pagination)

