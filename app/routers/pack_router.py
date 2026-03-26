from fastapi import APIRouter, HTTPException, status

from app.core.config import settings
from app.db.client import supabase
from app.schemas.catalog_schemas import PackOut


router = APIRouter(prefix="/packs", tags=["packs"])


@router.get("", response_model=list[PackOut], status_code=status.HTTP_200_OK)
def get_packs():
    character_table = settings.CHARACTER_TABLE_NAME

    select_query = (
        "id_pack,name,cost,"
        "probabilities:pack_probability(percentage,"
        "card:cards(id_card,number,"
        f"character:{character_table}(id_charapter,name,anime:animes(id_anime,title)),"
        "rarity:rarities(id_rarity,code,name),"
        "style:styles(id_style,name)"
        "))"
    )

    try:
        response = supabase.table("packs").select(select_query).execute()

        if response.data is None:
            return []

        packs: list[dict] = []
        for pack in response.data:
            probabilities = pack.get("probabilities") or []

            probability_items = []
            for probability in probabilities:
                card = probability.get("card") or {}
                character = card.get("character") or {}
                anime = character.get("anime") or {}
                rarity = card.get("rarity") or {}
                style = card.get("style") or {}

                probability_items.append(
                    {
                        "percentage": float(probability.get("percentage") or 0),
                        "card": {
                            "id_card": card.get("id_card"),
                            "number": card.get("number"),
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
                        },
                    }
                )

            packs.append(
                {
                    "id_pack": pack.get("id_pack"),
                    "name": pack.get("name"),
                    "cost": pack.get("cost"),
                    "probabilities": probability_items,
                }
            )

        return packs
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch packs: {exc}",
        ) from exc
