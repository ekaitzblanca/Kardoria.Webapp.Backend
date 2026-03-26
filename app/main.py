from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import card_router, pack_router, user_router

app = FastAPI()

app.add_middleware(
	CORSMiddleware,
	allow_origins=[
		"http://localhost:4200",
		"https://kardoria.netlify.app",
		"https://www.kardoria.netlify.app",
	],
	allow_origin_regex=r"https://.*\.netlify\.app",
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"],
)

app.include_router(user_router.router)
app.include_router(card_router.router)
app.include_router(pack_router.router)

