from fastapi import FastAPI, Request, Header, HTTPException
from fastapi.responses import JSONResponse
import json, os
from datetime import datetime
from dotenv import load_dotenv
import hmac, hashlib


load_dotenv()

app = FastAPI()


WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET")
print(WEBHOOK_SECRET)



@app.post("/pf/lead-created")
async def pf_lead_created(request: Request):
    # Read raw body (bytes)
    raw_body = await request.body()
    payload = json.loads(raw_body.decode("utf-8"))
    print(payload)

    # Verify signature
    signature = request.headers.get("X-Signature")
    if signature:
        computed = hmac.new(WEBHOOK_SECRET.encode(), raw_body, hashlib.sha256).hexdigest()

        if not hmac.compare_digest(signature, computed):
            print("❌ Signature mismatch")
            return JSONResponse({"error": "Invalid signature"}, status_code=401)

    print("✅ Signature verified")


    lead_id = payload.get("id")
    lead_type = payload.get("type")
    timestamp = payload.get("timestamp")
    entity = payload.get("entity", {})
    data = payload.get("payload", {})

    entity_id = entity.get("id")
    entity_type = entity.get("type")

    channel = data.get("channel")
    status = data.get("status")
    entity_type_detail = data.get("entityType")
    public_profile_id = data.get("publicProfile", {}).get("id")
    listing_id = data.get("listing", {}).get("id")
    listing_reference = data.get("listing", {}).get("reference")
    project_id = data.get("project", {}).get("id")
    developer_id = data.get("developer", {}).get("id")
    response_link = data.get("responseLink")

    sender = data.get("sender", {})
    sender_name = sender.get("name")
    contacts = sender.get("contacts", [])
    sender_phone = contacts[0]["value"] if contacts else None



    success = insert_lead({
        "lead_id": lead_id,
        "lead_type": lead_type,
        "timestamp": timestamp,
        "entity_id": entity_id,
        "entity_type": entity_type,
        "channel": channel,
        "status": status,
        "entity_type_detail": entity_type_detail,
        "public_profile_id": public_profile_id,
        "listing_id": listing_id,
        "listing_reference": listing_reference,
        "project_id": project_id,
        "developer_id": developer_id,
        "response_link": response_link,
        "sender_name": sender_name,
        "sender_phone": sender_phone
    }, DB_CONFIG)


    return JSONResponse(status_code=200, content={"status": "received"})



@app.get("/")
def read_root():
    return {"message": "PF Webhook, V1.2.0"}

if __name__ == "__main__":# or Run using: uvicorn cg-webhook:app --host 0.0.0.0 --port 8007 --reload
    import uvicorn
    #uvicorn.run("cg-webhook:app", host="0.0.0.0", port=8007, reload=True)# dev
    uvicorn.run(app, host="0.0.0.0", port=8007)# prod
