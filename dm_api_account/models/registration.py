from pydantic import BaseModel, Field, ConfigDict

class Registration(BaseModel):
    model_config = ConfigDict(extra="forbid")

    login: str = Field(..., description="The user's login")
    password: str = Field(..., description="The user's password")
    email: str = Field(..., description="The user's email")



