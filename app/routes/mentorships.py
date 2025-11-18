from fastapi import APIRouter, Depends, HTTPException
from app.db import get_supabase
from app.schemas.mentorship_schema import MentorshipCreate

router = APIRouter()

# CREATE
@router.post("/")
def create_mentorship(data: MentorshipCreate, supabase = Depends(get_supabase)):
    res = supabase.table("mentorships").insert({
        "mentor_name": data.mentor_name,
        "mentee_name": data.mentee_name
    }).execute()
    return res.data

# GET ALL
@router.get("/")
def get_all_mentorships(supabase = Depends(get_supabase)):
    return supabase.table("mentorships").select("*").execute().data

# GET SPECIFIC
@router.get("/{mentorship_id}")
def get_mentorship(mentorship_id: int, supabase = Depends(get_supabase)):
    res = supabase.table("mentorships").select("*").eq("id", mentorship_id).execute()
    if not res.data:
        raise HTTPException(status_code=404, detail="Mentorship not found")
    return res.data[0]

# UPDATE
@router.put("/{mentorship_id}")
def update_mentorship(mentorship_id: int, updates: dict, supabase = Depends(get_supabase)):
    res = supabase.table("mentorships").update(updates).eq("id", mentorship_id).execute()
    if not res.data:
        raise HTTPException(status_code=404, detail="Mentorship not found")
    return res.data[0]

# DELETE
@router.delete("/{mentorship_id}")
def delete_mentorship(mentorship_id: int, supabase = Depends(get_supabase)):
    res = supabase.table("mentorships").delete().eq("id", mentorship_id).execute()
    if not res.data:
        raise HTTPException(status_code=404, detail="Mentorship not found")
    return {"message": "Mentorship deleted"}
