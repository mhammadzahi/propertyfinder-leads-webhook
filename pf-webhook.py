from fastapi import FastAPI, Request, Header, HTTPException
from fastapi.responses import JSONResponse


import json, os
from datetime import datetime
from dotenv import load_dotenv

from functions.database import insert_lead

import hmac, hashlib


load_dotenv()

app = FastAPI()



DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT"),
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD")
}

WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET")

@app.post("/pf/lead-created")
async def pf_lead_created(request: Request):

    signature = request.headers.get("X-Signature")
    if signature:
        computed = hmac.new(WEBHOOK_SECRET.encode(), str(payload).encode(), hashlib.sha256).hexdigest()
        if not hmac.compare_digest(signature, computed):
            return JSONResponse({"error": "Invalid signature"}, status_code=401)


    payload = await request.json()
    print(payload)


    lead_id = payload.get("id")
    lead_type = payload.get("type")
    timestamp = payload.get("timestamp")
    entity = payload.get("entity", {})
    data = payload.get("payload", {})

    # Example extracted info
    sender_name = data.get("sender", {}).get("name")
    contact_list = data.get("sender", {}).get("contacts", [])
    listing_id = data.get("listing", {}).get("id")
    channel = data.get("channel")

    print(f"New lead received: {lead_id} from {sender_name} via {channel}")
    print(f"Listing ID: {listing_id}")
    print(f"Contacts: {contact_list}")

    #insert_lead(payload, DB_CONFIG)

    return JSONResponse(status_code=200, content={"status": "received"})



@app.get("/")
def read_root():
    return {"message": "PF Webhook, V1.1.0"}

if __name__ == "__main__":# or Run using: uvicorn cg-webhook:app --host 0.0.0.0 --port 8007 --reload
    import uvicorn
    #uvicorn.run("cg-webhook:app", host="0.0.0.0", port=8007, reload=True)# dev
    uvicorn.run(app, host="0.0.0.0", port=8007)# prod
