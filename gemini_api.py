import os
import requests
import streamlit as st




GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1/models/gemini-1.5-pro:generateContent"

def query_gemini(prompt, context=None):
    if not GOOGLE_API_KEY:
        return "❌ Error: API key not found. Please check your .env file."

    headers = {"Content-Type": "application/json"}
    body = {
        "contents": [
            {
                "role": "user",
                "parts": [
                    {"text": f"{context if context else ''}\n\nUser: {prompt}"}
                ]
            }
        ]
    }

    try:
        response = requests.post(
            f"{GEMINI_API_URL}?key={GOOGLE_API_KEY}",
            headers=headers,
            json=body
        )

        if response.status_code == 200:
            return response.json()["candidates"][0]["content"]["parts"][0]["text"]
        else:
            return f"❌ API Error:\n\n{response.text}"

    except Exception as e:
        return f"❌ Request failed: {e}"
    
def query_gemini_vision(base64_image, mime_type):
    headers = {"Content-Type": "application/json"}
    body = {
        "contents": [
            {
                "role": "user",
                "parts": [
                    {
                        "inline_data": {
                            "mime_type": mime_type,
                            "data": base64_image
                        }
                    },
                    {
                        "text": "Please analyze this medical image and extract any health-related insights."
                    }
                ]
            }
        ]
    }

    response = requests.post(
        "https://generativelanguage.googleapis.com/v1/models/gemini-1.5-pro-vision:generateContent"
        + f"?key={GOOGLE_API_KEY}",
        headers=headers,
        json=body
    )

    if response.status_code == 200:
        return response.json()["candidates"][0]["content"]["parts"][0]["text"]
    else:
        return f"❌ Vision API Error:\n{response.text}"

