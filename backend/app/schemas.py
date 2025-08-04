from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

# User 스키마
class UserBase(BaseModel):
    email: str
    username: str

class UserCreate(UserBase):
    password: str

class UserUpdate(UserBase):
    password: Optional[str] = None
    is_active: Optional[bool] = None

    class Config:
        from_attributes = True

class User(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

# schemas.py 하단에 추가 (또는 User와 비슷한 위치에)
class UserResponse(BaseModel):
    id: int
    email: str
    username: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True  # 또는 orm_mode = True, pydantic v2에서는 from_attributes


# Quiz 스키마
class QuizBase(BaseModel):
    category: str
    question: str
    options: List[str]
    correct_answer: int
    explanation: str

class QuizCreate(QuizBase):
    video_path: Optional[str] = None
    road_elements: Optional[List[str]] = None
    ai_generated: bool = False

class Quiz(QuizBase):
    id: int
    user_id: int
    video_path: Optional[str]
    road_elements: Optional[List[str]]
    ai_generated: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

# WrongAnswer 스키마
class WrongAnswerBase(BaseModel):
    user_answer: str

class WrongAnswerCreate(WrongAnswerBase):
    quiz_id: int

class WrongAnswer(WrongAnswerBase):
    id: int
    user_id: int
    quiz_id: int
    is_reviewed: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

# UserStats 스키마
class UserStatsBase(BaseModel):
    total_quizzes: int
    correct_answers: int
    streak: int
    level: str
    points: int

class UserStats(UserStatsBase):
    id: int
    user_id: int
    updated_at: datetime
    
    class Config:
        from_attributes = True

# VideoAnalysis 스키마
class VideoAnalysisBase(BaseModel):
    video_path: str
    road_elements: List[str]
    description: str
    category: str

class VideoAnalysisCreate(VideoAnalysisBase):
    pass

class VideoAnalysis(VideoAnalysisBase):
    id: int
    user_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# 인증 스키마
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: str

# API 응답 스키마
class QuizResponse(BaseModel):
    quiz: Quiz
    analysis: Optional[VideoAnalysis] = None

class QuizAnswer(BaseModel):
    selected_option: int
    
    class Config:
        from_attributes = True

class UserProfile(BaseModel):
    user: User
    stats: UserStats
    recent_quizzes: List[Quiz]
    wrong_answers_count: int 

class UserProfile(BaseModel):
    user:User
    stats : UserStats
    recent_quizzes: list[Quiz]