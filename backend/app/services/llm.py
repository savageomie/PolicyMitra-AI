
import os
import asyncio
from typing import Optional, Dict, Any, List

import httpx

SYSTEM_PROMPT = (
    "You are an insurance advisor for rural India. Provide accurate, simple, rural-friendly explanations, "
    "avoid jargon, avoid hallucination."
)

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GROQ_MODEL = "llama3-70b-8192"

def build_messages(message: str, context: Optional[dict]) -> List[dict]:
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ]
    if context and isinstance(context, dict) and context.get("messages"):
        messages.extend(context["messages"])
    messages.append({"role": "user", "content": message})
    return messages

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

async def generate_chat_response(message: str, context: Optional[dict] = None) -> str:
    """
    Groq-only chat response.
    """
    messages = build_messages(message, context)
    try:
        if not GROQ_API_KEY:
            raise ValueError("Missing GROQ_API_KEY")
        return await call_groq(messages)
    except Exception:
        return "Sorry, I am facing technical issues right now."


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
            summary = await generate_chat_response(prompt, context=None)
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
        eli5 = await generate_chat_response(eli5_prompt, context=None)
    except Exception:
        eli5 = "[ELI5 explanation unavailable]"

    return {"summary": raw_summary, "eli5": eli5}


    async def enhance_recommendations(plans: list, survey_data: dict) -> list:
        """
        Use the Groq LLM to:
          - refine explanations for each plan
          - assign a trust_score (0.0-1.0) with short reasoning
          - rewrite explanations in simple, rural Hindi

        Returns a list of dicts: [{name, refined_explanation, trust_score, trust_reason, hindi_explanation}, ...]
        Falls back to a simple heuristic if LLM call or parsing fails.
        """
        # Normalize input plans to simple dicts
        simple_plans = []
        for p in plans:
            if isinstance(p, dict):
                simple_plans.append({
                    "name": p.get("name"),
                    "reason": p.get("reason"),
                    "estimated_premium": p.get("estimated_premium")
                })
            else:
                # assume p is a Pydantic model or object with attributes
                simple_plans.append({
                    "name": getattr(p, "name", None),
                    "reason": getattr(p, "reason", None),
                    "estimated_premium": getattr(p, "estimated_premium", None)
                })

        prompt = (
            "You are an assistant that refines insurance plan recommendations for rural India. "
            "Given the following plans and the user's survey data, do three things for each plan:\n"
            "1) produce a short, clear refined explanation in simple English (1-2 sentences),\n"
            "2) assign a trust_score between 0.0 and 1.0 (higher means more confident) and give a one-line reason for the score,\n"
            "3) rewrite the refined explanation in simple rural Hindi (use very basic vocabulary).\n"
            "Return ONLY valid JSON: an object with a single key \"improved_plans\" whose value is an array of objects. "
            "Each object must contain the keys: name, refined_explanation, trust_score, trust_reason, hindi_explanation.\n\n"
            "Survey data:\n" + json.dumps(survey_data or {}, ensure_ascii=False) + "\n\n"
            "Plans:\n" + json.dumps(simple_plans, ensure_ascii=False) + "\n\n"
            "Output example:\n{\"improved_plans\":[{\"name\":\"Crop Insurance\",\"refined_explanation\":\"...\",\"trust_score\":0.85,\"trust_reason\":\"...\",\"hindi_explanation\":\"...\"}] }"
        )

        try:
            resp_text = await generate_chat_response(prompt, context=None)
            # Try to parse JSON from the LLM response
            try:
                data = json.loads(resp_text)
                improved = data.get("improved_plans")
                if isinstance(improved, list):
                    return improved
            except Exception:
                # attempt to extract JSON substring
                start = resp_text.find("{")
                end = resp_text.rfind("}")
                if start != -1 and end != -1 and end > start:
                    try:
                        data = json.loads(resp_text[start:end+1])
                        improved = data.get("improved_plans")
                        if isinstance(improved, list):
                            return improved
                    except Exception:
                        pass
        except Exception:
            # fall through to heuristic fallback
            pass

        # Fallback heuristic: create simple improved entries
        fallback = []
        occ = (survey_data.get("occupation") or "").lower() if survey_data else ""
        income = survey_data.get("income") if survey_data and isinstance(survey_data.get("income"), (int, float)) else None
        for p in simple_plans:
            name = p.get("name")
            reason = p.get("reason") or "Recommended"
            # basic trust scoring
            score = 0.6
            if occ and "farm" in occ and name and "crop" in name.lower():
                score += 0.2
            if income is not None and income < 15000 and "micro" in (name or "").lower():
                score += 0.15
            score = max(0.0, min(1.0, score))
            refined = f"{reason}. This plan is suggested based on your survey answers."
            hindi = f"(हिंदी) {reason}"
            fallback.append({
                "name": name,
                "refined_explanation": refined,
                "trust_score": round(score, 2),
                "trust_reason": "Heuristic fallback reasoning",
                "hindi_explanation": hindi
            })

        return fallback