from app.db.client import supabase

def get_users():
    response = supabase.table("users").select("*").execute()
    return response.data