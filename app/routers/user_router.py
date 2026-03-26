from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.db.client import supabase

router = APIRouter()


class LoginRequest(BaseModel):
    email: str
    password: str

@router.get("/users")
def get_users():
    return supabase.table("users").select("id_user,name,email,username").execute()


@router.post("/login")
def login(payload: LoginRequest):
    response = (
        supabase.table("users")
        .select("id_user,name,email,username,password")
        .eq("email", payload.email)
        .limit(1)
        .execute()
    )

    if not response.data:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    user = response.data[0]
    if user.get("password") != payload.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return {
        "message": "Login successful",
        "user": {
            "id_user": user.get("id_user"),
            "name": user.get("name"),
            "email": user.get("email"),
            "username": user.get("username"),
        },
    }