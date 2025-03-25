
import google.generativeai as genai
genai.configure(api_key="<your key>")  # Replace with your actual API key
def detect_primary_intent(email_body):
    """Detects primary intent when multiple requests are present."""

    model = genai.GenerativeModel("gemini-2.0-pro-exp-02-05")

    prompt = f"""
    Analyze the following email and extract all request types. 
    Identify the **primary request** that represents the sender's main intent.

    Email Content:
    {email_body}
    Output the primary request type, other requests, and reasoning.
    """
    response = model.generate_content(prompt)
    return response.text  # Extracted primary intent


