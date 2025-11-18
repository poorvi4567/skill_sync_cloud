from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import users, skills, opportunities, mentorships

app = FastAPI(
    title="SkillSync Backend (Supabase)",
    version="1.0.0"
)

# ---------------- CORS (Important for frontend) ----------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],      # change this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------- ROUTERS ----------------
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(skills.router, prefix="/skills", tags=["Skills"])
app.include_router(opportunities.router, prefix="/opportunities", tags=["Opportunities"])
app.include_router(mentorships.router, prefix="/mentorships", tags=["Mentorships"])

# ---------------- HEALTH CHECK ----------------
@app.get("/")
def root():
    return {"message": "SkillSync Backend is running 🚀"}
