from pydantic import BaseModel, Field, ConfigDict

class LoginCredentials(BaseModel):
    model_config = ConfigDict(extra="forbid")

    login: str = Field(..., description="The user's login")
    password: str = Field(..., description="The user's password")
    remember_me: bool = Field(..., description="Whether or not the user is logged in", serialization_alias="rememberMe")