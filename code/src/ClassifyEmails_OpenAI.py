import openai
from FetchMails import get_latest_email

email_data = get_latest_email()

openai.api_key = "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"


def classify_email(email_text):
    prompt = f"""
    Classify the email into:
    - Request Type
    - Sub Request Type
    - Confidence Score (0-100)

    Email:
    {email_text}

    Output JSON: {{"request_type": "", "sub_request_type": "", "confidence": ""}}

"""
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": "You classify loan servicing emails."},
                  {"role": "user", "content": prompt}],
        temperature=0.5
    )

    return response["choices"][0]["message"]["content"]


classification = classify_email(email_data["body"])
print(classification)
