from fastapi import APIRouter, HTTPException
from app.services.weaviate_client import get_weaviate_client, init_weaviate_schema
import weaviate
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

@router.get("/status")
async def check_weaviate_status():
    """Weaviate 연결 상태 확인"""
    try:
        client = get_weaviate_client()
        if client and client.is_ready():
            return {"status": "connected", "message": "Weaviate is ready"}
        return {"status": "disconnected", "message": "Weaviate is not available"}
    except Exception as e:
        logger.error(f"Weaviate connection error: {str(e)}")
        raise HTTPException(status_code=503, detail=f"Weaviate connection error: {str(e)}")

@router.post("/init")
async def initialize_weaviate():
    """Weaviate 스키마 초기화"""
    try:
        success = init_weaviate_schema()
        if success:
            return {"status": "success", "message": "Weaviate schema initialized"}
        return {"status": "failed", "message": "Failed to initialize Weaviate schema"}
    except Exception as e:
        logger.error(f"Weaviate schema initialization error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Weaviate schema initialization error: {str(e)}")

@router.post("/add-quiz")
async def add_quiz_to_weaviate(quiz_data: dict):
    """Weaviate에 퀴즈 벡터 추가"""
    try:
        client = get_weaviate_client()
        if not client:
            raise HTTPException(status_code=503, detail="Weaviate is not available")

        # 퀴즈 데이터 벡터화 및 저장
        quiz_vector = client.data_object.create({
            "question": quiz_data.get("question", ""),
            "category": quiz_data.get("category", ""),
            "difficulty": quiz_data.get("difficulty", "")
        }, "Quiz")

        return {"status": "success", "message": "Quiz added to Weaviate", "vector_id": quiz_vector}
    except Exception as e:
        logger.error(f"Error adding quiz to Weaviate: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error adding quiz: {str(e)}")

@router.get("/search-quiz")
async def search_quiz_in_weaviate(query: str):
    """Weaviate에서 퀴즈 검색"""
    try:
        client = get_weaviate_client()
        if not client:
            raise HTTPException(status_code=503, detail="Weaviate is not available")

        # 벡터 검색
        result = client.query.get("Quiz", ["question", "category", "difficulty"]) \
            .with_near_text({"concepts": [query]}) \
            .with_limit(5) \
            .do()

        return {"status": "success", "results": result.get("data", {}).get("Get", {}).get("Quiz", [])}
    except Exception as e:
        logger.error(f"Error searching quiz in Weaviate: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error searching quiz: {str(e)}")