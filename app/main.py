import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from app.routes import users, skills, opportunities, mentorships, opportunity_skills, user_skills, match, chat, resume_ats

import logging
# Suppress the passlib/bcrypt version warning
logging.getLogger('passlib').setLevel(logging.ERROR)
# Load environment variables (for local dev)
load_dotenv()

app = FastAPI(
    title="SkillSync Backend",
    version="2.0.0",
    description="Complete mentorship platform"
)


# ---------------- CORS ----------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------- ROUTERS ----------------
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(skills.router, prefix="/skills", tags=["Skills"])
app.include_router(opportunities.router, prefix="/opportunities", tags=["Opportunities"])
app.include_router(mentorships.router)
app.include_router(opportunity_skills.router, prefix="/opportunity-skills", tags=["Opportunity Skills"])
app.include_router(user_skills.router)
app.include_router(match.router, prefix="/match", tags=["Matching"])
app.include_router(chat.router)  # WebSocket chat - NO PREFIX
app.include_router(resume_ats.router)

@app.get("/config")
def get_config():
    """Serve public configuration to frontend"""
    return {
        "SUPABASE_URL": os.getenv("SUPABASE_URL"),
        "SUPABASE_ANON_KEY": os.getenv("SUPABASE_ANON_KEY")
    }

# ---------------- FRONTEND MOUNTING ----------------
# Resolve path: main.py is in /app/app/, frontend is in /app/frontend/
current_dir = os.path.dirname(os.path.abspath(__file__)) 
root_dir = os.path.dirname(current_dir) 
frontend_path = os.path.join(root_dir, "frontend")

# Mount the frontend to the root "/"
app.mount("/", StaticFiles(directory=frontend_path, html=True), name="frontend")
