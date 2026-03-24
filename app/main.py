from fastapi import FastAPI
from supabase import create_client
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Conectar a Supabase
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "API de prueba con Supabase"}

@app.get("/users")
def get_users():
    # Reemplaza "users" por el nombre de tu tabla
    response = supabase.table("users").select("*").execute()
    return response.data