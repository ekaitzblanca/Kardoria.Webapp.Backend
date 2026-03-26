from fastapi import APIRouter, HTTPException, status

from app.core.config import settings
from app.db.client import supabase
from app.schemas.catalog_schemas import CardOut


router = APIRouter(prefix="/cards", tags=["cards"])


@router.get("", response_model=list[CardOut], status_code=status.HTTP_200_OK)
def get_cards():
    try:
        select_query = (
            "id_card,number,"
            "character:charapters(id_charapter,name,anime:animes(id_anime,title)),"
            "rarity:rarities(id_rarity,code,name),"
            "style:styles(id_style,name)"
        )

        response = supabase.table("cards").select(select_query).execute()

        if response.data is None:
            return []

        cards: list[dict] = []
        for row in response.data:
            character = row.get("character") or {}
            anime = character.get("anime") or {}
            rarity = row.get("rarity") or {}
            style = row.get("style") or {}

            cards.append(
                {
                    "id_card": row.get("id_card"),
                    "number": row.get("number"),
                    "character": {
                        "id_character": character.get("id_charapter"),
                        "name": character.get("name"),
                        "anime": {
                            "id_anime": anime.get("id_anime"),
                            "title": anime.get("title"),
                        },
                    },
                    "rarity": {
                        "id_rarity": rarity.get("id_rarity"),
                        "code": rarity.get("code"),
                        "name": rarity.get("name"),
                    },
                    "style": {
                        "id_style": style.get("id_style"),
                        "name": style.get("name"),
                    },
                }
            )

        return cards
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch cards: {exc}",
        ) from exc
