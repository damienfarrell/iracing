from pydantic import BaseModel

class RaceDataInput(BaseModel):
    session_id: int
    passcode: int

class RaceDataResponse(BaseModel):
    session_id: int
    session_name: str
    status: str