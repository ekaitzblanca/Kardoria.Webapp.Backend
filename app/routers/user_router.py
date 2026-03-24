from fastapi import APIRouter
from app.db.client import supabase

router = APIRouter()

@router.get("/users")
def get_users():
    return supabase.table("users").select("*").execute()