from fastapi import FastAPI
from FetchMails import authenticate, fetch_latest_email
from ClassifyEmails_GeminiAI import classify_email
from Detect_MultipleIntents import detect_primary_intent

# Initialize FastAPI app
app = FastAPI()

@app.get("/")
def root():
    return {"message": "GenAI Email Processing API is running!"}

# 🔹 Endpoint 1: Fetch Emails
@app.get("/fetch-emails")
def fetch_emails(email: str, password: str):
    emails = fetch_latest_email(email,password)
    if emails:
        return {"emails": emails}
    return {"message": "No new emails found."}

# 🔹 Endpoint 2: Classify an Email
@app.post("/classify-email")
def classify(subject: str, body: str):
    classification_result = classify_email(subject, body)
    return {
        "subject": subject,
        "classification": classification_result
    }

# 🔹 Endpoint 3: Detect Intent in Email
@app.post("/detect-intent")
def detect_intent(body: str):
    intent_result = detect_primary_intent(body)
    return {
        "email_body": body,
        "primary_intent": intent_result
    }

# Run the API
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
