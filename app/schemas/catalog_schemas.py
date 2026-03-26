from pydantic import BaseModel


class CharacterOut(BaseModel):
    id_character: int
    name: str
    anime: "AnimeOut"


class AnimeOut(BaseModel):
    id_anime: int
    title: str


class RarityOut(BaseModel):
    id_rarity: int
    code: str
    name: str


class StyleOut(BaseModel):
    id_style: int
    name: str


class CardOut(BaseModel):
    id_card: int
    number: str
    character: CharacterOut
    rarity: RarityOut
    style: StyleOut


class PackCardOut(BaseModel):
    percentage: float
    card: CardOut


class PackOut(BaseModel):
    id_pack: int
    name: str
    cost: int
    probabilities: list[PackCardOut]
