import os
from langchain_google_genai import ChatGoogleGenerativeAI


def get_llm(temperature=0.3):
    return ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key=os.getenv("GOOGLE_API_KEY"),
        temperature=temperature,
        convert_system_message_to_human=True,
    )