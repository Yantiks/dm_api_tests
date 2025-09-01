from pydantic import BaseModel, Field, ConfigDict

class ResetPassword(BaseModel):
    model_config = ConfigDict(extra="forbid")

    login: str = Field(..., description="The user's login")
    email: str = Field(..., description="The user's email")
