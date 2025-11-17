
import os
import asyncio
from typing import Optional, Dict, Any, List

import httpx

SYSTEM_PROMPT = (
    "You are an insurance advisor for rural India. Provide accurate, simple, rural-friendly explanations, "
    "avoid jargon, avoid hallucination."
)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")

OPENAI_MODEL = "gpt-4o-mini"  # or "gpt-4.1"
GROQ_MODEL = "llama3-70b-8192"

def build_messages(message: str, context: Optional[dict]) -> List[dict]:
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ]
    if context and isinstance(context, dict) and context.get("messages"):
        messages.extend(context["messages"])
    messages.append({"role": "user", "content": message})
    return messages

async def call_openai(messages: List[dict]) -> str:
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": OPENAI_MODEL,
        "messages": messages,
        "temperature": 0.7,
        "max_tokens": 512
    }
    async with httpx.AsyncClient(timeout=30) as client:
        resp = await client.post(url, headers=headers, json=payload)
        resp.raise_for_status()
        data = resp.json()
        return data["choices"][0]["message"]["content"].strip()

async def call_groq(messages: List[dict]) -> str:
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": GROQ_MODEL,
        "messages": messages,
        "temperature": 0.7,
        "max_tokens": 512
    }
    async with httpx.AsyncClient(timeout=30) as client:
        resp = await client.post(url, headers=headers, json=payload)
        resp.raise_for_status()
        data = resp.json()
        return data["choices"][0]["message"]["content"].strip()

async def generate_chat_response(
    message: str,
    context: Optional[dict] = None,
    provider: str = "openai"
) -> str:
    """
    Unified LLM chat response for OpenAI and Groq.
    """
    messages = build_messages(message, context)
    try:
        if provider == "openai":
            if not OPENAI_API_KEY:
                raise ValueError("Missing OPENAI_API_KEY")
            return await call_openai(messages)
        elif provider == "groq":
            if not GROQ_API_KEY:
                raise ValueError("Missing GROQ_API_KEY")
            return await call_groq(messages)
        else:
            raise ValueError(f"Unknown provider: {provider}")
    except Exception:
        return "Sorry, I am facing technical issues right now."