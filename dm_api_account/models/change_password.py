from pydantic import BaseModel, Field, ConfigDict

class ChangePassword(BaseModel):
    model_config = ConfigDict(extra="forbid")

    login: str = Field(..., description="The user's login")
    token: str = Field(..., description="The user's token")
    oldpassword: str = Field(..., description="The user's old password", serialization_alias="oldPassword")
    newpassword: str = Field(..., description="The user's new password", serialization_alias="newPassword")