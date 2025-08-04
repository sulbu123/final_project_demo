from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from typing import Optional
import logging

from app.database import get_db
from app.models import User, UserStats
from app.schemas import UserCreate, UserResponse, Token, TokenData
from app.core.config import settings

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

# 비밀번호 해싱
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 설정
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def get_user(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def authenticate_user(db: Session, email: str, password: str):
    user = get_user(db, email)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except JWTError:
        raise credentials_exception
    user = get_user(db, email=token_data.email)
    if user is None:
        raise credentials_exception
    return user

@router.post("/register", response_model=UserResponse)
async def register(request: Request, user: UserCreate, db: Session = Depends(get_db)):
    logger.info(f"Register attempt for email: {user.email}")
    try:
        # 요청 바디 로깅
        body = await request.json()
        logger.info(f"Request body: {body}")
    except:
        pass

    # 이메일 중복 확인
    db_user = get_user(db, email=user.email)
    if db_user:
        logger.warning(f"Email already registered: {user.email}")
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # 사용자명 중복 확인
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        logger.warning(f"Username already taken: {user.username}")
        raise HTTPException(status_code=400, detail="Username already taken")
    
    try:
        # 새 사용자 생성
        hashed_password = get_password_hash(user.password)
        db_user = User(
            email=user.email,
            username=user.username,
            hashed_password=hashed_password,
            is_active=True
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        
        # 초기 사용자 통계 생성
        user_stats = UserStats(user_id=db_user.id)
        db.add(user_stats)
        db.commit()
        
        logger.info(f"Successfully registered user: {user.email}")
        return db_user
    except Exception as e:
        logger.error(f"Error during registration: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Internal server error during registration")

@router.post("/login", response_model=Token)
async def login(request: Request, form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    logger.info(f"Login attempt for username: {form_data.username}")
    try:
        # 요청 바디 로깅
        body = await request.body()
        logger.info(f"Request body: {body}")
    except:
        pass

    try:
        user = authenticate_user(db, form_data.username, form_data.password)
        if not user:
            logger.warning(f"Failed login attempt for username: {form_data.username}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.email}, expires_delta=access_token_expires
        )
        
        logger.info(f"Successful login for user: {form_data.username}")
        return {"access_token": access_token, "token_type": "bearer"}
    except Exception as e:
        logger.error(f"Error during login: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error during login")

@router.get("/me", response_model=UserResponse)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user