# app/main.py (FIXED for WebSocket & Indentation)
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import users, skills, opportunities, mentorships, opportunity_skills, user_skills, match, chat, resume_ats
from app.utils.firebase_chat_db import get_firebase_chat_db
import os
from fastapi.staticfiles import StaticFiles

app = FastAPI(
    title="SkillSync Backend (Firebase + Supabase)",
    version="2.0.0",
    description="Complete mentorship platform with Resume ATS Scorer"
)

@app.on_event("startup")
async def startup_event():
    # Initialize Firebase
    try:
        get_firebase_chat_db()
        print("✅ Firebase initialized")
    except Exception as e:
        print(f"⚠️ Firebase initialization failed: {e}")
        import traceback
        traceback.print_exc()

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

# ---------------- DEBUG: List all routes ----------------
@app.on_event("startup")
async def show_routes():
    print("\n📋 Registered Routes:")
    for route in app.routes:
        if hasattr(route, 'methods'):
            methods = ', '.join(route.methods)
            print(f"  [{methods}] {route.path}")
        else:
            print(f"  {route.path}")
    print()

# ---------------- FRONTEND MOUNTING ----------------
# Resolve path: main.py is in /app/app/, frontend is in /app/frontend/
current_dir = os.path.dirname(os.path.abspath(__file__)) 
root_dir = os.path.dirname(current_dir) 
frontend_path = os.path.join(root_dir, "frontend")

# Mount the frontend to the root "/"
app.mount("/", StaticFiles(directory=frontend_path, html=True), name="frontend")
