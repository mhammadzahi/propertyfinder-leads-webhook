import psycopg2
from psycopg2 import sql



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

    try:
        payload = lead_json.get("payload", {})
        entity = lead_json.get("entity", {})
        sender = payload.get("sender", {})
        contacts = sender.get("contacts", [])

        phone = None
        for c in contacts:
            if c.get("type") == "phone":
                phone = c.get("value")
                break

        data = {
            "lead_id": lead_json.get("id"),
            "lead_type": lead_json.get("type"),
            "timestamp": lead_json.get("timestamp"),
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
        print(f"Error inserting lead: {e}")
        return False




if __name__ == "__main__":
    sample_lead = {
        "id": "lead-created-12345678",
        "type": "lead.created",
        "timestamp": "2019-08-24T14:15:22Z",
        "entity": {"id": "string", "type": "lead"},
        "payload": {
            "channel": "whatsapp",
            "status": "sent",
            "entityType": "listing",
            "publicProfile": {"id": 123},
            "listing": {
                "id": "01JZ50J63YP6BZB49N0BZ8M3T6",
                "reference": "01JZ50J63YP6BZB49N0BZ8M3T6"
            },
            "project": {"id": "123e4567-e89b-12d3-a456-426655440000"},
            "developer": {"id": "123e4567-e89b-12d3-a456-426655440000"},
            "responseLink": "https://example.com",
            "sender": {
                "name": "Jane Doe",
                "contacts": [{"type": "phone", "value": "+971555555555"}]
            }
        }
    }



    success = insert_lead(sample_lead, db_config)
  
