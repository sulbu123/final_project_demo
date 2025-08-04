from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User
from app.schemas import UserResponse, UserUpdate
from app.routers.auth import get_current_user

router = APIRouter()

@router.get("/profile", response_model=UserResponse)
def get_user_profile(
    current_user: User = Depends(get_current_user)
):
    """사용자 프로필 조회"""
    return current_user

@router.put("/profile", response_model=UserResponse)
def update_user_profile(
    user_update: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """사용자 프로필 업데이트"""
    # 사용자명 중복 확인
    if user_update.username and user_update.username != current_user.username:
        existing_user = db.query(User).filter(
            User.username == user_update.username,
            User.id != current_user.id
        ).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="Username already taken")
    
    # 이메일 중복 확인
    if user_update.email and user_update.email != current_user.email:
        existing_user = db.query(User).filter(
            User.email == user_update.email,
            User.id != current_user.id
        ).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")
    
    # 프로필 업데이트
    if user_update.username:
        current_user.username = user_update.username
    if user_update.email:
        current_user.email = user_update.email
    
    db.commit()
    db.refresh(current_user)
    
    return current_user 