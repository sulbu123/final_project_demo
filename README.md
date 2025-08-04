# 도로 주행 퀴즈 서비스 🚗

AI 기반 도로 주행 영상 분석 및 퀴즈 생성 서비스입니다. 자율주행 차량이 주행 중 마주치는 다양한 교통 상황을 바탕으로, 멀티모달 AI 모델이 영상 정보를 텍스트로 변환하고, 이를 기반으로 LLM이 도로교통법에 맞는 퀴즈를 생성합니다.

## 기술 스택 🛠️

| 구성 요소 | 기술 스택 |
|----------|-----------|
| 프론트엔드 | React |
| 백엔드 | FastAPI |
| 관계형 DB | MariaDB |
| 벡터 DB | Weaviate |
| 비동기 처리 | Celery + Redis |
| 벡터 생성 모델 | OpenAI, CLIP, Sentence-BERT |

## 프로젝트 구조 📁

```
아이고UI/
├── frontend/                # React 프론트엔드
│   ├── src/
│   │   ├── components/     # 공통 컴포넌트
│   │   ├── contexts/       # Context API (인증 등)
│   │   ├── pages/         # 페이지 컴포넌트
│   │   ├── services/      # API 서비스
│   │   ├── App.js         # 메인 앱 컴포넌트
│   │   └── index.js       # 진입점
│   ├── public/            # 정적 파일
│   └── package.json       # 프론트엔드 의존성
│
├── backend/                # FastAPI 백엔드
│   ├── app/
│   │   ├── core/          # 설정, 유틸리티
│   │   ├── routers/       # API 라우터
│   │   ├── services/      # 비즈니스 로직
│   │   ├── models.py      # DB 모델
│   │   ├── schemas.py     # Pydantic 스키마
│   │   └── database.py    # DB 설정
│   ├── main.py            # FastAPI 앱
│   └── Dockerfile         # 백엔드 도커파일
│
├── requirements.txt        # Python 의존성
└── docker-compose.yml     # 도커 컴포즈 설정
```

## 주요 기능 ⭐

### 1. 홈 대시보드
- 학습 진행도 확인
- 최근 퀴즈 결과
- 오늘의 학습 목표

### 2. 퀴즈 기능
- AI 기반 퀴즈 생성
  - 영상 업로드 및 분석
  - 상황별 퀴즈 자동 생성
- 기존 퀴즈 풀기
  - 카테고리별 퀴즈
  - 답변 제출 및 채점

### 3. 오답노트
- 틀린 문제 복습
- 해설 및 관련 법규 확인
- 카테고리별 취약점 분석

### 4. 학습분석
- 학습 통계 대시보드
- 카테고리별 성과
- 학습 추세 분석

### 5. 내정보
- 프로필 관리
- 학습 설정
- 진행 상황 확인

## 데이터베이스 구조 💾

### MariaDB 테이블
1. **users**
   - 사용자 정보 관리
   - 인증 및 권한 관리

2. **quizzes**
   - 퀴즈 문제 저장
   - AI 생성 퀴즈 관리

3. **wrong_answers**
   - 오답 기록
   - 복습 관리

4. **user_stats**
   - 학습 통계
   - 성과 추적

5. **video_analyses**
   - 영상 분석 결과
   - AI 생성 설명

### Weaviate 컬렉션
- 퀴즈 벡터 저장
- 유사 문제 검색
- 컨텍스트 기반 추천




## 개발 현황 🔄

### 완료된 기능
- ✅ 프로젝트 구조 설정
- ✅ 데이터베이스 모델 설계
- ✅ 기본 인증 시스템
- ✅ React 컴포넌트 구현
- ✅ FastAPI 엔드포인트 구현

### 진행 중인 작업
- 🔄 AI 모델 통합
- 🔄 Weaviate 벡터 검색
- 🔄 Celery 작업 큐 설정

### 예정된 작업
- 📝 테스트 코드 작성
- 📝 성능 최적화
- 📝 배포 파이프라인 구축

## 기여 방법 💡
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 라이선스 📄
This project is licensed under the MIT License - see the LICENSE file for details. 
