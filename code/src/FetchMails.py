import requests
import os
import time
import google.generativeai as genai
import base64
import re
import pytesseract
from pdf2image import convert_from_path
genai.configure(api_key="<Key>")  # Replace with your actual API key

# 🔹 Define Function to Classify Email with Gemini API
BASE_URL = "https://api.mail.tm"
TEMP_EMAIL = "<your mail>"  # Replace with your temp email
TEMP_PASSWORD = "<password>"  # Replace with your temp email password
ATTACHMENT_FOLDER = "<download path>" # Folder where the mail attachments are stored if found
EXTRACTEDTEXT_FOLDER = "<extracted text path>" # Folder where the OCR extracted text is stored as text file

# Ensure attachment and extracted text folders exists
if not os.path.exists(ATTACHMENT_FOLDER):
    os.makedirs(ATTACHMENT_FOLDER)
if not os.path.exists(EXTRACTEDTEXT_FOLDER):
    os.makedirs(EXTRACTEDTEXT_FOLDER)
def authenticate(email, password):
    """Authenticate and get a session token."""
    response = requests.post(f"{BASE_URL}/token", json={
        "address": email,
        "password": password
    })

    if response.status_code == 200:
        return response.json()["token"]
    else:
        raise Exception("❌ Authentication failed. Check email/password.")

def fetch_latest_email(email_arg,password_arg):
    """Fetch the latest email details from inbox."""
    token = authenticate(email_arg,password_arg)
    Fetched_Emails = [] # all email details stored and returned as a list
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/messages", headers=headers)

    if response.status_code == 200:
        emails = response.json()["hydra:member"]
        if emails:
            for email in emails:
                latest_email_id = email["id"]
                email_details = requests.get(f"{BASE_URL}/messages/{latest_email_id}", headers=headers).json()
                Fetched_Emails.append(email_details) # add current mail details to result
                CurrentMail_Attachments = download_attachments(email_details,token)
                for file in CurrentMail_Attachments:
                    if file.endswith(".pdf"):
                        print(f"\n🔍 Extracting text from: {file}")
                        pdf_text = extract_text_using_gemini(file)[0]
                        Filename = re.sub(r'[^\w\-_]', '_', email_details['subject']) + "_" + \
                                   os.path.splitext(os.path.basename(file))[0] + ".txt"
                        file_path = os.path.join(EXTRACTEDTEXT_FOLDER, Filename)
                        with open(file_path, "w", encoding="utf-8") as text_file:
                            text_file.write(pdf_text)
                        print("✅ Extracted Text:\n", pdf_text)
                    else:
                        print("No downloads")
            return Fetched_Emails  # Returning full email details
        else:
            return None
    else:
        raise Exception("❌ Failed to fetch emails.")

def download_attachments(email_details, token):
    """Download attachments from the email if any exist."""
    headers = {"Authorization": f"Bearer {token}"}
    attachments = email_details.get("attachments", [])
    message_id = email_details["id"]
    subject = re.sub(r'[^\w\-_]', '',email_details['subject'])
    downloaded_files = []
    if attachments:
        for attachment in attachments:
            attachment_id = attachment["id"]
            filename = attachment["filename"]
            file_url = f"{BASE_URL}/messages/{message_id}/attachment/{attachment_id}"

            response = requests.get(file_url, headers=headers)

            if response.status_code == 200:
                file_path = os.path.join(ATTACHMENT_FOLDER,filename)
                with open(file_path, "wb") as f:
                    f.write(response.content)
                print(f"✅ Attachment saved: {file_path}")
                downloaded_files.append(file_path)
    return downloaded_files

def encode_pdf_to_base64(pdf_path):
    with open(pdf_path, "rb") as pdf_file:
        return base64.b64encode(pdf_file.read()).decode("utf-8")

#Send PDF to Gemini AI for Text Extraction
def extract_text_using_gemini(pdf_path):
    encoded_pdf = encode_pdf_to_base64(pdf_path)

    # model = genai.GenerativeModel("gemini-2.0-pro-exp-02-05")  # Use vision model
    model = genai.GenerativeModel("gemini-2.0-flash-lite")

    response = model.generate_content([
        "Extract all text from this PDF:",
        {"mime_type": "application/pdf", "data": encoded_pdf}
    ])

    return [response.text,encoded_pdf]

