from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List

from app.database import get_db
from app.models import User, UserStats, WrongAnswer, Quiz
from app.routers.auth import get_current_user

router = APIRouter()

@router.get("/stats")
def get_user_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """사용자 통계 조회"""
    # 사용자 통계 조회 또는 생성
    user_stats = db.query(UserStats).filter(UserStats.user_id == current_user.id).first()
    
    if not user_stats:
        # 통계가 없으면 생성
        user_stats = UserStats(
            user_id=current_user.id,
            total_quizzes=0,
            correct_answers=0,
            streak=0,
            level="초급",
            points=0
        )
        db.add(user_stats)
        db.commit()
        db.refresh(user_stats)
    
    return user_stats

@router.get("/wrong-answers")
def get_wrong_answers(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """오답노트 조회"""
    wrong_answers = db.query(WrongAnswer).filter(
        WrongAnswer.user_id == current_user.id
    ).all()
    
    return wrong_answers

@router.get("/progress")
def get_learning_progress(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """학습 진행도 조회"""
    # 총 퀴즈 수
    total_quizzes = db.query(Quiz).filter(Quiz.user_id == current_user.id).count()
    
    # 정답 수
    correct_answers = db.query(WrongAnswer).filter(
        WrongAnswer.user_id == current_user.id
    ).count()
    
    # 정답률 계산
    accuracy = (correct_answers / total_quizzes * 100) if total_quizzes > 0 else 0
    
    return {
        "total_quizzes": total_quizzes,
        "correct_answers": correct_answers,
        "accuracy": round(accuracy, 1),
        "level": "초급" if accuracy < 70 else "중급" if accuracy < 90 else "고급"
    } 