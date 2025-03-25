from FetchMails import *
from ClassifyEmails_GeminiAI import *
from Detect_MultipleIntents import *

TEMP_EMAIL = "<Your email>"  # Replace with your temp email
TEMP_PASSWORD = "<email password>"  # Replace with your temp email password

latest_emails = fetch_latest_email(TEMP_EMAIL,TEMP_PASSWORD) # Fetching the mails from mailbox
for item in latest_emails:
    classification_result = classify_email(item["subject"],item["text"]) # classify the current mail request type
    PrimaryIntent = detect_primary_intent(item["text"]) # identify the primary and other intents
    print("=============================================")
    print("")
    print("\n✅ Classification Result for mail with subject : "+item["subject"])
    print(classification_result)
    print("\n✅ Intent Result for mail with subject : " + item["subject"])
    print(PrimaryIntent)