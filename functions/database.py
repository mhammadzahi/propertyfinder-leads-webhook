import psycopg2
from datetime import datetime

def insert_lead(lead_json, db_config):
    sql_insert = """
        INSERT INTO pf_leads (
            lead_id, lead_type, timestamp, entity_id, entity_type,
            channel, status, entity_type_detail, public_profile_id,
            listing_id, listing_reference, project_id, developer_id,
            response_link, sender_name, sender_phone
        )
        VALUES (
            %(lead_id)s, %(lead_type)s, %(timestamp)s, %(entity_id)s, %(entity_type)s,
            %(channel)s, %(status)s, %(entity_type_detail)s, %(public_profile_id)s,
            %(listing_id)s, %(listing_reference)s, %(project_id)s, %(developer_id)s,
            %(response_link)s, %(sender_name)s, %(sender_phone)s
        )
        ON CONFLICT (lead_id) DO NOTHING;
    """

    conn = None
    try:
        payload = lead_json.get("payload", {})
        entity = lead_json.get("entity", {})
        sender = payload.get("sender", {})
        contacts = sender.get("contacts", [])

        phone = next((c.get("value") for c in contacts if c.get("type") == "phone"), None)

        # Convert timestamp to datetime
        ts = lead_json.get("timestamp")
        if ts:
            ts = datetime.fromisoformat(ts.replace("Z", "+00:00"))

        data = {
            "lead_id": lead_json.get("id"),
            "lead_type": lead_json.get("type"),
            "timestamp": ts,
            "entity_id": entity.get("id"),
            "entity_type": entity.get("type"),
            "channel": payload.get("channel"),
            "status": payload.get("status"),
            "entity_type_detail": payload.get("entityType"),
            "public_profile_id": payload.get("publicProfile", {}).get("id"),
            "listing_id": payload.get("listing", {}).get("id"),
            "listing_reference": payload.get("listing", {}).get("reference"),
            "project_id": payload.get("project", {}).get("id"),
            "developer_id": payload.get("developer", {}).get("id"),
            "response_link": payload.get("responseLink"),
            "sender_name": sender.get("name"),
            "sender_phone": phone
        }

        with psycopg2.connect(**db_config) as conn:
            with conn.cursor() as cur:
                cur.execute(sql_insert, data)
                conn.commit()

        print(f"✅ Lead inserted: {data['lead_id']}")
        return True

    except Exception as e:
        print(f"❌ Error inserting lead: {e}")
        if conn:
            conn.rollback()
        return False

