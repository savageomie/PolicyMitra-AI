from fastapi import APIRouter, HTTPException
from ..models.schemas import RecommendRequest, RecommendResponse, Plan

router = APIRouter()


@router.post("/recommend", response_model=RecommendResponse)
async def recommend(req: RecommendRequest):
    """Simple rule-based recommendation engine.

    Inputs: occupation, income, family_size
    Rules:
      - If occupation == 'farmer' -> Crop Insurance
      - If family_size > 3 -> Family Health Plan
      - If income < 15000 -> Micro Insurance

    Returns list of plans, trust_score, total_premium, and explanation.
    """
    occ = (req.occupation or "").strip().lower()
    income = req.income
    family_size = req.family_size

    plans: list[Plan] = []

    # Rule: farmer -> Crop Insurance
    if occ == "farmer":
        plans.append(Plan(name="Crop Insurance", reason="Occupation is farmer", estimated_premium=2000.0))

    # Rule: family size > 3 -> Family Health Plan
    if family_size > 3:
        plans.append(Plan(name="Family Health Plan", reason="Large family size", estimated_premium=5000.0))

    # Rule: low income -> micro-insurance
    if income < 15000:
        plans.append(Plan(name="Micro Insurance", reason="Low income", estimated_premium=300.0))

    # If no rules matched, provide a safe default recommendation
    if not plans:
        plans.append(Plan(name="Standard Life Cover", reason="No specific rule matched; generic protection", estimated_premium=1500.0))

    total_premium = sum(p.estimated_premium or 0.0 for p in plans)

    # Simple trust score heuristic: higher for lower income (needs protection) and for farmers
    trust_score = 0.7
    if occ == "farmer":
        trust_score += 0.1
    # adjust by family size modestly
    trust_score += min(0.15, 0.01 * max(0, family_size - 1))
    # lower income => slightly higher priority/trust
    if income < 15000:
        trust_score += 0.05
    # clamp
    trust_score = max(0.0, min(1.0, trust_score))

    # Build an explanation string
    reasons = [f"{p.name}: {p.reason or 'recommended'} (premium ₹{p.estimated_premium:.2f})" for p in plans]
    explanation = "; ".join(reasons)

    return RecommendResponse(plans=plans, trust_score=round(trust_score, 2), total_premium=round(total_premium, 2), explanation=explanation)