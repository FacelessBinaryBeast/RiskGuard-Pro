# underwriting_agent.py
# Backend for Dynamic Underwriting and Risk Assessment Agent

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Optional
import uvicorn

app = FastAPI(title="Dynamic Underwriting Agent")
templates = Jinja2Templates(directory="templates")

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# ---------------------------- Models ----------------------------
class UserInput(BaseModel):
    name: str
    age: int
    location: str
    occupation: str
    steps_per_day: Optional[int] = 0
    bmi: Optional[float] = None
    smoker: bool
    pre_existing_conditions: Optional[str] = None

class RiskAssessment(BaseModel):
    risk_level: str
    summary: str
    recommended_cover: float
    suggested_premium: float
    deductible: float
    recommended_riders: Optional[str]

# ---------------------------- Logic ----------------------------
def assess_risk(data: UserInput) -> RiskAssessment:
    risk_score = 0
    reasons = []
    tips = []

    # ---- Age Factor ----
    if data.age < 30:
        risk_score += 1
        reasons.append("You are under 30, which is generally associated with lower health risks.")
    elif data.age < 50:
        risk_score += 2
        reasons.append("Your age is between 30 and 50, which represents moderate age-related health risk.")
    else:
        risk_score += 3
        reasons.append("Being over 50 increases your risk due to age-related health conditions.")
        tips.append("Consider annual health checkups and increase your emergency fund allocation.")

    # ---- Occupation Risk ----
    high_risk_jobs = ["driver", "construction", "delivery", "miner"]
    if any(job in data.occupation.lower() for job in high_risk_jobs):
        risk_score += 3
        reasons.append(f"Your occupation as a {data.occupation} is considered high-risk due to physical exposure or accident probability.")
        tips.append("Consider adding Personal Accident Cover to your policy.")
    else:
        reasons.append(f"Your occupation as a {data.occupation} is considered low-risk.")

    # ---- Activity Level ----
    if data.steps_per_day < 5000:
        risk_score += 2
        reasons.append("Low physical activity (<5,000 steps/day) increases lifestyle-related health risks.")
        tips.append("Aim for at least 7,000–10,000 steps/day to reduce risk and improve premiums.")
    elif data.steps_per_day < 10000:
        risk_score += 1
        reasons.append("Moderate physical activity helps but can be improved.")
    else:
        reasons.append("Excellent physical activity (>10,000 steps/day) reduces lifestyle-related risks.")

    # ---- BMI Check ----
    if data.bmi:
        if data.bmi < 18.5 or data.bmi > 30:
            risk_score += 2
            reasons.append(f"Your BMI of {data.bmi} falls in a risk range (underweight or obese).")
            tips.append("Maintaining a BMI between 18.5–24.9 helps reduce future complications.")

    # ---- Smoking ----
    if data.smoker:
        risk_score += 3
        reasons.append("Smoking significantly increases the risk of cardiovascular and respiratory issues.")
        tips.append("Quitting smoking for even 6 months can positively impact your future premiums.")

    # ---- Health Conditions ----
    if data.pre_existing_conditions:
        risk_score += 2
        reasons.append(f"Declared pre-existing condition: {data.pre_existing_conditions}. This increases your risk profile.")
        tips.append("Disclose all medical history accurately to avoid future claim rejections.")

    # ---- Final Risk Level & Policy Suggestion ----
    if risk_score <= 3:
        level = "Low"
        cover = 1000000.0
        premium = 350.0
        deductible = 10000.0
    elif risk_score <= 6:
        level = "Moderate"
        cover = 750000.0
        premium = 550.0
        deductible = 25000.0
    else:
        level = "High"
        cover = 500000.0
        premium = 850.0
        deductible = 50000.0

    riders = "Critical Illness + Accidental Cover" if level != "Low" else "Accidental Cover"

    # ---- Final Natural-Language Summary ----
    summary = (
        f"📄 **Risk Level**: {level}\n\n"
        f"🔍 **Assessment Reasoning**:\n"
        + "\n".join([f"- {r}" for r in reasons]) +
        "\n\n💡 **Suggested Improvements**:\n" +
        ( "\n".join([f"- {tip}" for tip in tips]) if tips else "- Keep up the healthy habits!" ) +
        "\n\n📑 **Policy Recommendation**:\n"
        f"- Suggested Sum Insured: ₹{int(cover)}\n"
        f"- Monthly Premium: ₹{int(premium)}\n"
        f"- Deductible: ₹{int(deductible)}\n"
        f"- Add-on Riders: {riders}"
    )

    return RiskAssessment(
        risk_level=level,
        summary=summary,
        recommended_cover=cover,
        suggested_premium=premium,
        deductible=deductible,
        recommended_riders=riders
    )


# ---------------------------- Route ----------------------------
@app.post("/assess_risk", response_model=RiskAssessment)
def get_risk_report(user_data: UserInput):
    try:
        return assess_risk(user_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/", response_class=HTMLResponse)
def serve_home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/basics", response_class=HTMLResponse)
def serve_basics(request: Request):
    return templates.TemplateResponse("basics.html", {"request": request})

@app.get("/additional", response_class=HTMLResponse)
def serve_additional(request: Request):
    return templates.TemplateResponse("additional.html", {"request": request})

@app.get("/familydetails", response_class=HTMLResponse)
def serve_family_details(request: Request):
    return templates.TemplateResponse("familydetails.html", {"request": request})

@app.get("/finances", response_class=HTMLResponse)
def serve_finances(request: Request):
    return templates.TemplateResponse("finances.html", {"request": request})

@app.get("/coverage", response_class=HTMLResponse)
def serve_coverage(request: Request):
    return templates.TemplateResponse("coverage.html", {"request": request})

@app.get("/medical", response_class=HTMLResponse)
def serve_medical(request: Request):
    return templates.TemplateResponse("medical.html", {"request": request})

@app.get("/preferences", response_class=HTMLResponse)
def serve_preferences(request: Request):
    return templates.TemplateResponse("preferences.html", {"request": request})

# ---------------------------- Main ----------------------------
if __name__ == "__main__":
    uvicorn.run("underwriting_agent:app", host="0.0.0.0", port=8000, reload=True)