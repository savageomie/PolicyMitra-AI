
async def summarize_policy(text: str) -> dict:
    """
    Summarize policy text in chunks, then create a rural-friendly ELI5 explanation.
    Returns: { 'summary': ..., 'eli5': ... }
    """
    # 1. Chunk text
    chunk_size = 1500
    chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]
    summaries = []
    for chunk in chunks:
        prompt = (
            "Summarize the following insurance policy text in simple, clear language for rural India. "
            "Avoid jargon.\n\nText:\n" + chunk
        )
        try:
            summary = await generate_chat_response(prompt, context=None, provider="openai")
        except Exception:
            summary = "[Summary unavailable]"
        summaries.append(summary)
    raw_summary = "\n".join(summaries)

    # 4. ELI5 rural-language version
    eli5_prompt = (
        "Explain the following insurance policy summary as if I am 5 years old, "
        "using rural Indian language and examples. Avoid jargon.\n\nSummary:\n" + raw_summary
    )
    try:
        eli5 = await generate_chat_response(eli5_prompt, context=None, provider="openai")
    except Exception:
        eli5 = "[ELI5 explanation unavailable]"

    return {"summary": raw_summary, "eli5": eli5}

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