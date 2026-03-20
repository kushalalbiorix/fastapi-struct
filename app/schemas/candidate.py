from pydantic import BaseModel, EmailStr, Field, model_validator


class CreateUserRequest(BaseModel):
    """Request model for creating a new user."""
    email: EmailStr = Field(..., description="User email address", example="user@example.com")
    
    
class LoginUserRequest(BaseModel):
    """Request model for login user."""
    email: EmailStr = Field(..., description="User Email Address", example="user@examples.com")
    password: str = Field(..., description="User Password",example="Example@1234")
    

    
class RefreshToken(BaseModel):
    token: str = Field(..., description="refresh token")
    
    
class VerifyToken(BaseModel):
    token: str = Field(..., description="verify token")
    
class ForgetPassword(BaseModel):
    email: EmailStr = Field(...,description="Email Address." , example= "user@example.com")
    
    
class ResetPassword(BaseModel):
    token: str = Field(..., description="Password reset token", example="reset_token_here")
    
class UpdatePassword(BaseModel):
    token: str = Field(..., description="Password reset token", example="reset_token_here")
    new_password: str = Field(...,description="New password", example="Demo@1234")
    verfiy_password: str = Field(...,description="Verify password", example= "Demo@1234")

    @model_validator(mode="after")
    def passwords_match(self):
        if self.new_password != self.verfiy_password:
            raise ValueError("Passwords do not match")
        return self