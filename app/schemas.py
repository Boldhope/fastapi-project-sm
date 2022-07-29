from pydantic import BaseModel, EmailStr, conint
from typing import Optional
from datetime import datetime

# define a model for validation (schema)
# Should always define needed data and response model
# Note we can have different schemas (to provide select pieces of information) for different path operations

# Post Create Schemas
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass

# User Response Model
class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime   
    
    class Config:
        orm_mode = True

# User Request Schema
class UserCreate(BaseModel):
    email: EmailStr
    password: str

# Login Request Schema
class UserLogin(BaseModel):
    email: EmailStr
    password: str

# Post Response model
class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut
    # The below is needed because we are returning SQLAlchemy model, not pydantic model
    class Config:
        orm_mode = True

# Note to self, the names for the entries of the schema are important. It is important to match the name with the information in the query.
class PostOut(BaseModel):
    Post: Post
    votes: int

    class Config:
        orm_mode = True

# Vote Request Model
class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)

# Token Schemas
class Token(BaseModel):
    access_token: str
    token_type: str
    
class TokenData(BaseModel):
    id: Optional[str]
