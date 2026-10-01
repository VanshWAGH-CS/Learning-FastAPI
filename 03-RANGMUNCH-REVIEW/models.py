from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class Review(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    play_name: str = Field(index=True)
    reviewer_name: str
    rating: int = Field(ge=1, le=5)  # Rating should be between 1 and 5
    comment: str
    created_at: datetime = Field(default_factory=datetime.utcnow)


class ReviewCreate(SQLModel):
    play_name: str
    reviewer_name: str
    rating: int = Field(ge=1, le=5)  # Rating should be between 1 and 5
    comment: str


class ReviewRead(SQLModel):
    id: int
    play_name: str
    reviewer_name: str
    rating: int
    comment: str
    created_at: datetime


class ReviewUpdate(SQLModel):
    play_name: Optional[str] = None
    reviewer_name: Optional[str] = None
    rating: Optional[int] = Field(default=None, ge=1, le=5)  # Rating should be between 1 and 5
    comment: Optional[str] = None