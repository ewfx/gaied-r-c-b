import requests
import time

BASE_URL = "https://api.mail.tm"

# Enter your manually created temp email and password
TEMP_EMAIL = "756ministerial@indigobook.com"
TEMP_PASSWORD = "Klp`<tkU[1"


def authenticate(email, password):
    """Authenticate and get a session token."""
    response = requests.post(f"{BASE_URL}/token", json={
        "address": email,
        "password": password
    })

    if response.status_code == 200:
        return response.json()["token"]
    else:
        raise Exception("Authentication failed. Check your email and password.")


def fetch_latest_email(token):
    """Fetch the latest email from the temporary inbox."""
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/messages", headers=headers)

    if response.status_code == 200:
        emails = response.json()["hydra:member"]
        if emails:
            latest_email_id = emails[0]["id"]
            email_details = requests.get(f"{BASE_URL}/messages/{latest_email_id}", headers=headers).json()
            return {
                "subject": email_details["subject"],
                "body": email_details["text"]
            }
        else:
            return {"subject": None, "body": None}
    else:
        raise Exception("Failed to fetch emails.")

def get_latest_email():
    return {"subject": latest_email["subject"], "body": latest_email["body"]}

# Authenticate using manually created email
auth_token = authenticate(TEMP_EMAIL, TEMP_PASSWORD)

# Fetch latest email (wait a few seconds if needed for emails to arrive)
time.sleep(5)
latest_email = fetch_latest_email(auth_token)

print("\nLatest Email:")
print("Subject:", latest_email["subject"])
print("Body:", latest_email["body"])
