from fastapi import APIRouter, Depends, HTTPException
from app.db import get_supabase
from app.schemas.opportunity_schema import OpportunityCreate

router = APIRouter()

# CREATE
@router.post("/")
def create_opportunity(opp: OpportunityCreate, supabase = Depends(get_supabase)):
    res = supabase.table("opportunities").insert({
        "title": opp.title,
        "description": opp.description,
        "posted_by": opp.posted_by,
        "type": opp.type
    }).execute()
    return res.data

# READ ALL
@router.get("/")
def get_all_opportunities(supabase = Depends(get_supabase)):
    return supabase.table("opportunities").select("*").execute().data

# READ ONE
@router.get("/{opp_id}")
def get_opportunity(opp_id: str, supabase = Depends(get_supabase)):
    res = supabase.table("opportunities").select("*").eq("opp_id", opp_id).execute()
    if not res.data:
        raise HTTPException(status_code=404, detail="Opportunity not found")
    return res.data[0]

# UPDATE
@router.put("/{opp_id}")
def update_opportunity(opp_id: str, updates: dict, supabase = Depends(get_supabase)):
    res = supabase.table("opportunities").update(updates).eq("opp_id", opp_id).execute()
    if not res.data:
        raise HTTPException(status_code=404, detail="Opportunity not found")
    return res.data[0]

# DELETE
@router.delete("/{opp_id}")
def delete_opportunity(opp_id: str, supabase = Depends(get_supabase)):
    res = supabase.table("opportunities").delete().eq("opp_id", opp_id).execute()
    if not res.data:
        raise HTTPException(status_code=404, detail="Opportunity not found")
    return {"message": "Opportunity deleted"}
