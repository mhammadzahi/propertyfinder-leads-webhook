from fastapi import FastAPI, Request, Header, HTTPException
from fastapi.responses import JSONResponse
import json, os

from dotenv import load_dotenv
load_dotenv()

# import hmac, hashlib

from functions.send_to_lambda import send_to_lambda



app = FastAPI()


WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET")
LAMBDA_URL = os.getenv("LAMBDA_URL")
LAMBDA_API_KEY = os.getenv("LAMBDA_API_KEY")

# print(WEBHOOK_SECRET)



@app.post("/pf/lead-created")
async def pf_lead_created(request: Request):
    raw_body = await request.body()
    payload = json.loads(raw_body.decode("utf-8"))


    # signature = request.headers.get("X-Signature")
    # if signature:
    #     computed = hmac.new(WEBHOOK_SECRET.encode(), raw_body, hashlib.sha256).hexdigest()

    #     if not hmac.compare_digest(signature, computed):
    #         print("Signature mismatch")
    #         return JSONResponse({"error": "Invalid signature"}, status_code=401)

    # print("Signature verified")

    lead_data = {
        "lead_id": payload.get("id"),
        "lead_type": payload.get("type"),
        "timestamp": payload.get("timestamp"),
        "entity_id": payload.get("entity", {}).get("id"),
        "entity_type": payload.get("entity", {}).get("type"),
        "channel": payload.get("payload", {}).get("channel"),
        "status": payload.get("payload", {}).get("status"),
        "entity_type_detail": payload.get("payload", {}).get("entityType"),
        "public_profile_id": payload.get("payload", {}).get("publicProfile", {}).get("id"),
        "listing_id": payload.get("payload", {}).get("listing", {}).get("id"),
        "listing_reference": payload.get("payload", {}).get("listing", {}).get("reference"),
        "project_id": payload.get("payload", {}).get("project", {}).get("id"),
        "developer_id": payload.get("payload", {}).get("developer", {}).get("id"),
        "response_link": payload.get("payload", {}).get("responseLink"),
        "sender_name": payload.get("payload", {}).get("sender", {}).get("name"),
        "sender_phone": (payload.get("payload", {}).get("sender", {}).get("contacts") or [{}])[0].get("value")
    }
    print(lead_data)

    success = send_to_lambda(lead_data, LAMBDA_URL, LAMBDA_API_KEY)
    return JSONResponse(status_code=200, content={"status": "received"})



@app.get("/")
def read_root():
    return {"message": "PF Webhook, V1.2.0"}

if __name__ == "__main__":# or Run using: uvicorn cg-webhook:app --host 0.0.0.0 --port 8007 --reload
    import uvicorn
    #uvicorn.run("cg-webhook:app", host="0.0.0.0", port=8007, reload=True)# dev
    uvicorn.run(app, host="0.0.0.0", port=8007)# prod
