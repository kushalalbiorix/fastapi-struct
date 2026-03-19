from pydantic import BaseModel, EmailStr, Field


class CreateUserRequest(BaseModel):
    """Request model for creating a new user."""
    email: EmailStr = Field(..., description="User email address", example="user@example.com")
    
    
class LoginUserRequest(BaseModel):
    """Request model for login user."""
    email: EmailStr = Field(..., description="User Email Address", example="user@examples.com")
    password: str = Field(..., description="User Password",example="Example@1234")
    

    
class RefreshToken(BaseModel):
    
    token: str = Field(..., description="refresh token")
    