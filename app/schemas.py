from pydantic import BaseModel

class GroupCreate(BaseModel):
    name: str
    price: str | None = None
    time: str | None = None
    place: str | None = None



class ParticipantCreate(BaseModel):
    name: str
    suggestion: str | None = None