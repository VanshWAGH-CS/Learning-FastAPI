from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select, func
from models import Review, ReviewCreate, ReviewRead, ReviewUpdate
from databse import get_session

router = APIRouter(prefix="/reviews", tags=["reviews"])

@router.post("/", response_model=ReviewRead)
def create_review(review: ReviewCreate, session: Session = Depends(get_session)):
    db_review = Review.from_orm(review)
    session.add(db_review)
    session.commit()
    session.refresh(db_review)
    return db_review    

@router.get("/", response_model=list[ReviewRead])
def list_reviews(
    play_name: str | None =  Query(default=None, description="Filter reviews by play name"),
    session: Session = Depends(get_session)
    skip: int = Query(default=0, ge=0, description="Number of reviews to skip"),
    limit: int = Query(default=10, ge=1, description="Maximum number of reviews to return"),    

    
):
query = select(Review)
if play_name:
    query = query.where(Review.play_name == play_name)  
