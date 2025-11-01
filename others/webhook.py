# send the webhook url to PF via API

import requests
import json


def subscribe_to_webhook(access_token, event_id, callback_url, secret):
    url = "https://atlas.propertyfinder.com/v1/webhooks"
    payload = {
        "eventId": event_id,
        "callbackUrl": callback_url,
        "secret": secret
    }
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    print("Status Code:", response.status_code)
    print("Response Body:", response.text)
    return response.json()


if __name__ == "__main__":
    ACCESS_TOKEN = ""
    SECRET = ""
    result = subscribe_to_webhook(
        access_token=ACCESS_TOKEN,
        event_id="lead.created",
        callback_url="https://leads.miramaruae.com/pf/lead-created",
        secret=SECRET
    )
    print(result)

    # output :
    # #Status Code: 201
    # Response Body: {"createdAt":"2025-10-24 13:59:43.469840541 +0000 UTC m=+8.175332239","eventId":"lead.created_c1c809c3-3a73-4142-aa12-01078d935311","url":"https://leads.miramaruae.com/pf/lead-created"}
    # {'createdAt': '2025-10-24 13:59:43.469840541 +0000 UTC m=+8.175332239', 'eventId': 'lead.created_c1c809c3-3a73-4142-aa12-01078d935311', 'url': 'https://leads.miramaruae.com/pf/lead-created'}
    # #
