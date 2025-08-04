import weaviate
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

def get_weaviate_client():
    try:
        client = weaviate.Client(
            url=settings.WEAVIATE_URL,
        )
        # 연결 테스트
        if client.is_ready():
            logger.info("Successfully connected to Weaviate")
            return client
        else:
            logger.error("Weaviate is not ready")
            return None
    except Exception as e:
        logger.error(f"Failed to connect to Weaviate: {str(e)}")
        return None

def init_weaviate_schema():
    """
    Weaviate 스키마 초기화
    - Quiz 클래스 생성 (문제 벡터 저장)
    """
    client = get_weaviate_client()
    if not client:
        return False

    try:
        # Quiz 클래스 스키마
        quiz_class = {
            "class": "Quiz",
            "description": "도로 주행 퀴즈 문제",
            "vectorizer": "text2vec-transformers",
            "moduleConfig": {
                "text2vec-transformers": {
                    "model": "sentence-transformers/paraphrase-multilingual-mpnet-base-v2",
                    "poolingStrategy": "mean",
                    "vectorizeClassName": False
                }
            },
            "properties": [
                {
                    "name": "question",
                    "dataType": ["text"],
                    "description": "퀴즈 문제",
                    "moduleConfig": {
                        "text2vec-transformers": {
                            "skip": False,
                            "vectorizePropertyName": False
                        }
                    }
                },
                {
                    "name": "category",
                    "dataType": ["text"],
                    "description": "퀴즈 카테고리"
                },
                {
                    "name": "difficulty",
                    "dataType": ["text"],
                    "description": "문제 난이도"
                }
            ]
        }

        # 기존 스키마가 있는지 확인
        if not client.schema.exists("Quiz"):
            client.schema.create_class(quiz_class)
            logger.info("Quiz class schema created successfully")

        return True

    except Exception as e:
        logger.error(f"Failed to initialize Weaviate schema: {str(e)}")
        return False