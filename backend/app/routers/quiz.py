from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List, Optional
import json

from app.database import get_db
from app.models import Quiz, User, WrongAnswer
from app.schemas import QuizCreate, QuizResponse, QuizAnswer
from app.routers.auth import get_current_user

router = APIRouter()

@router.get("/", response_model=List[QuizResponse])
def get_quizzes(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """퀴즈 목록 조회"""
    quizzes = db.query(Quiz).offset(skip).limit(limit).all()
    return quizzes

@router.get("/{quiz_id}", response_model=QuizResponse)
def get_quiz(
    quiz_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """특정 퀴즈 조회"""
    quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
    if quiz is None:
        raise HTTPException(status_code=404, detail="Quiz not found")
    return quiz

@router.post("/", response_model=QuizResponse)
def create_quiz(
    quiz: QuizCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """퀴즈 생성"""
    db_quiz = Quiz(
        user_id=current_user.id,
        category=quiz.category,
        question=quiz.question,
        options=json.dumps(quiz.options),
        correct_answer=quiz.correct_answer,
        explanation=quiz.explanation,
        video_path=quiz.video_path,
        road_elements=json.dumps(quiz.road_elements) if quiz.road_elements else None
    )
    db.add(db_quiz)
    db.commit()
    db.refresh(db_quiz)
    return db_quiz

@router.post("/{quiz_id}/answer")
def submit_answer(
    quiz_id: int,
    answer: QuizAnswer,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """퀴즈 답변 제출"""
    quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
    if quiz is None:
        raise HTTPException(status_code=404, detail="Quiz not found")
    
    # 정답 확인
    is_correct = answer.user_answer == quiz.correct_answer
    
    # 오답노트에 저장 (틀렸을 경우)
    if not is_correct:
        wrong_answer = WrongAnswer(
            user_id=current_user.id,
            quiz_id=quiz_id,
            user_answer=str(answer.user_answer)
        )
        db.add(wrong_answer)
    
    db.commit()
    
    return {
        "is_correct": is_correct,
        "correct_answer": quiz.correct_answer,
        "explanation": quiz.explanation
    }

@router.post("/generate")
async def generate_ai_quiz(
    video: UploadFile = File(...),
    category: str = Form(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """AI 퀴즈 생성 (임시 구현)"""
    # TODO: 실제 AI 모델 연동
    # 현재는 임시 퀴즈 생성
    
    # 임시 퀴즈 데이터
    temp_quiz = {
        "id": 999,
        "question": "교차로에서 우회전할 때 가장 안전한 방법은?",
        "options": [
            "빨리 우회전하기",
            "왼쪽을 확인하고 천천히 우회전하기",
            "신호등만 보고 우회전하기", 
            "다른 차량이 없으면 무시하고 우회전하기"
        ],
        "correct_answer": 1,
        "explanation": "우회전 시에는 반드시 왼쪽을 확인하고 천천히 우회전해야 합니다. 특히 보행자와 자전거를 주의해야 합니다.",
        "category": category
    }
    
    return {
        "quiz": temp_quiz,
        "message": "AI 퀴즈가 생성되었습니다! (임시 데이터)"
    } 