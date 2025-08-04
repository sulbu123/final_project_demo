from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, ForeignKey, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True)
    username = Column(String(100), unique=True, index=True)
    hashed_password = Column(String(255))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # 관계
    quizzes = relationship("Quiz", back_populates="user")
    wrong_answers = relationship("WrongAnswer", back_populates="user")
    user_stats = relationship("UserStats", back_populates="user", uselist=False)

class Quiz(Base):
    __tablename__ = "quizzes"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    category = Column(String(100))
    question = Column(Text)
    options = Column(Text)  # JSON 형태로 저장
    correct_answer = Column(Integer)
    explanation = Column(Text)
    video_path = Column(String(500), nullable=True)
    road_elements = Column(Text, nullable=True)  # JSON 형태로 저장
    ai_generated = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # 관계
    user = relationship("User", back_populates="quizzes")
    wrong_answers = relationship("WrongAnswer", back_populates="quiz")

class WrongAnswer(Base):
    __tablename__ = "wrong_answers"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    quiz_id = Column(Integer, ForeignKey("quizzes.id"))
    user_answer = Column(String(255))
    is_reviewed = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # 관계
    user = relationship("User", back_populates="wrong_answers")
    quiz = relationship("Quiz", back_populates="wrong_answers")

class UserStats(Base):
    __tablename__ = "user_stats"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    total_quizzes = Column(Integer, default=0)
    correct_answers = Column(Integer, default=0)
    streak = Column(Integer, default=0)
    level = Column(String(50), default="초급")
    points = Column(Integer, default=0)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # 관계
    user = relationship("User", back_populates="user_stats")

class VideoAnalysis(Base):
    __tablename__ = "video_analyses"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    video_path = Column(String(500))
    road_elements = Column(Text)  # JSON 형태로 저장
    description = Column(Text)
    category = Column(String(100))
    created_at = Column(DateTime(timezone=True), server_default=func.now()) 