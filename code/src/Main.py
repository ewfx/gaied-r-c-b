from FetchMails import *
from ClassifyEmails_GeminiAI import *
from Detect_MultipleIntents import *

TEMP_EMAIL = "756ministerial@indigobook.com"  # Replace with your temp email
TEMP_PASSWORD = "Klp`<tkU[1"  # Replace with your temp email password

auth_token = authenticate(TEMP_EMAIL, TEMP_PASSWORD)
latest_emails = fetch_latest_email(auth_token)
for item in latest_emails:
    classification_result = classify_email(item["subject"],item["text"])
    PrimaryIntent = detect_primary_intent(item["text"])
    print("\n✅ Classification Result for mail with subject : "+item["subject"])
    print(classification_result)
    print("\n✅ Intent Result for mail with subject : " + item["subject"])
    print(PrimaryIntent)