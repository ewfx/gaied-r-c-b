import google.generativeai as genai
import json


# 🔹 Set your Gemini API Key
genai.configure(api_key="AIzaSyBbVsDnDDQRMiLwrJlYZ48FqzU8i4Nkphc")  # Replace with your actual API key

#
# models = genai.list_models()
#
# print("✅ Available Models:")
# for model in models:
#     print(model.name)
# 🔹 Define Function to Classify Email with Gemini API
def classify_email(subject, body):

    results = []
    """Classify the email using Google Gemini AI."""
    prompt = f"""
    You are an AI that classifies banking service request emails into predefined request types.
    Analyze the following email and provide the best-matching request type and sub-request type.

    📩 Email Subject: {subject}
    📩 Email Body: {body}

    Provide the response in JSON format:
    {{
        "request_type": "<Main Request Type>",
        "sub_request_type": "<Sub Request Type>",
        "confidence": "<Confidence Score (0-100%)>"
    }}
    """

    model = genai.GenerativeModel("gemini-2.0-flash-lite")
    response = model.generate_content(prompt)

    if response and hasattr(response, "_result"):
        text_response = response._result.candidates[0].content.parts[0].text
        text_response = text_response.strip().replace("```json", "").replace("```", "").strip()
        try:
            # ✅ Extract values
            parsed_json = json.loads(text_response)

            # ✅ Extract values
            request_type = parsed_json.get("request_type", "Unknown")
            sub_request_type = parsed_json.get("sub_request_type", "Unknown")
            confidence = parsed_json.get("confidence", "Unknown")

            results.extend([request_type,sub_request_type,confidence])
            return results

        except json.JSONDecodeError as e:
            print(f"❌ JSON Parsing Error: {e}")
    else:
        print("❌ No valid response received.")


