import requests, json



def send_to_lambda(lead_data, lambda_url, lambda_api_key):
    headers = {
        "Content-Type": "application/json",
        "x-api-key": lambda_api_key
    }
    try:
        response = requests.post(lambda_url, headers=headers, data=json.dumps(lead_data))
        if response.status_code == 200:
            print("Data sent to Lambda successfully.")
            return True

        else:
            print(f"Failed to send data to Lambda. Status code: {response.status_code}, Response: {response.text}")
            return False

    except requests.exceptions.RequestException as e:
        print(f"Exception occurred while sending data to Lambda: {e}")
        return False
