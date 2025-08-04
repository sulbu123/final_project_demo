import cv2
import numpy as np
from PIL import Image
import torch
from transformers import pipeline
import openai
import json
import os
from typing import List, Dict, Any
from app.core.config import settings
import weaviate
from sentence_transformers import SentenceTransformer

class AIService:
    def __init__(self):
        """AI 서비스 초기화"""
        self.openai_client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
        
        # Weaviate 클라이언트 초기화
        self.weaviate_client = weaviate.Client(settings.WEAVIATE_URL)
        
        # 이미지 분석 모델
        self.image_analyzer = pipeline("image-classification", model="microsoft/resnet-50")
        
        # 텍스트 임베딩 모델
        self.text_embedder = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
        
        # 도로교통법 관련 키워드
        self.traffic_keywords = {
            "신호 및 표지": ["신호등", "도로표지", "신호체계", "빨간불", "초록불", "노란불"],
            "교차로 통과": ["교차로", "우회전", "좌회전", "직진", "보행자", "우선순위"],
            "주차 및 정차": ["주차", "정차", "주차장", "주차금지", "출입구"],
            "고속도로": ["고속도로", "진입", "진출", "속도제한", "차선변경"],
            "특수상황": ["긴급차량", "장애인", "어린이", "보호구역", "학교"]
        }
    
    def analyze_video_frame(self, frame: np.ndarray) -> List[str]:
        """비디오 프레임 분석"""
        try:
            # 프레임을 PIL 이미지로 변환
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            pil_image = Image.fromarray(frame_rgb)
            
            # 이미지 분석
            results = self.image_analyzer(pil_image)
            
            # 도로 관련 요소 추출
            road_elements = []
            for result in results:
                if any(keyword in result['label'].lower() for keyword in ['car', 'road', 'traffic', 'signal', 'crossing', 'vehicle']):
                    road_elements.append(result['label'])
            
            return road_elements
        except Exception as e:
            print(f"프레임 분석 오류: {e}")
            return []
    
    def analyze_video_file(self, video_path: str) -> List[str]:
        """비디오 파일 분석"""
        try:
            cap = cv2.VideoCapture(video_path)
            frames_analyzed = 0
            all_elements = []
            
            while cap.isOpened() and frames_analyzed < 10:  # 최대 10프레임 분석
                ret, frame = cap.read()
                if not ret:
                    break
                
                elements = self.analyze_video_frame(frame)
                all_elements.extend(elements)
                frames_analyzed += 1
            
            cap.release()
            
            # 중복 제거
            unique_elements = list(set(all_elements))
            return unique_elements
            
        except Exception as e:
            print(f"비디오 분석 오류: {e}")
            return []
    
    def generate_scenario_description(self, road_elements: List[str]) -> str:
        """도로 상황 설명 생성"""
        try:
            prompt = f"""
            다음 도로 요소들이 감지되었습니다: {', '.join(road_elements)}
            
            이 상황을 바탕으로 도로교통법에 관련된 상황 설명을 생성해주세요.
            설명은 한국어로 작성하고, 도로교통법과 관련된 내용을 포함해야 합니다.
            """
            
            response = self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "당신은 도로교통법 전문가입니다. 도로 상황을 분석하여 명확하고 교육적인 설명을 제공합니다."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=200,
                temperature=0.7
            )
            
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"상황 설명 생성 오류: {e}")
            return "도로 상황이 감지되었습니다. 안전 운전에 주의하세요."
    
    def generate_quiz_from_description(self, description: str, category: str) -> Dict[str, Any]:
        """설명을 바탕으로 퀴즈 생성"""
        try:
            prompt = f"""
            다음 도로 상황 설명을 바탕으로 도로교통법 퀴즈를 생성해주세요:
            
            상황: {description}
            카테고리: {category}
            
            다음 형식으로 JSON 응답을 제공해주세요:
            {{
                "question": "퀴즈 질문",
                "options": ["보기1", "보기2", "보기3", "보기4"],
                "correct": 0,
                "explanation": "정답 설명"
            }}
            
            퀴즈는 도로교통법에 관련된 내용이어야 하며, 4개의 보기 중 하나의 정답이 있어야 합니다.
            """
            
            response = self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "당신은 도로교통법 교육 전문가입니다. 명확하고 교육적인 퀴즈를 생성합니다."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=300,
                temperature=0.8
            )
            
            # JSON 응답 파싱
            try:
                quiz_data = json.loads(response.choices[0].message.content.strip())
                return quiz_data
            except json.JSONDecodeError:
                return self.generate_default_quiz(category)
                
        except Exception as e:
            print(f"퀴즈 생성 오류: {e}")
            return self.generate_default_quiz(category)
    
    def generate_default_quiz(self, category: str) -> Dict[str, Any]:
        """기본 퀴즈 생성 (AI 실패 시)"""
        default_quizzes = {
            "신호 및 표지": {
                "question": "빨간 신호등에서 우회전하려고 할 때, 다음 중 올바른 행동은?",
                "options": [
                    "보행자가 없으면 바로 우회전한다",
                    "보행자가 있으면 보행자가 건너기를 기다린 후 우회전한다",
                    "신호가 바뀔 때까지 기다린다",
                    "경찰관의 지시를 받는다"
                ],
                "correct": 1,
                "explanation": "빨간 신호에서 우회전할 때는 보행자가 있으면 보행자가 건너기를 기다린 후 우회전해야 합니다."
            },
            "교차로 통과": {
                "question": "신호등이 없는 교차로에서 좌회전하려고 할 때, 다음 중 우선순위가 높은 것은?",
                "options": [
                    "직진하는 차량",
                    "우회전하는 차량",
                    "보행자",
                    "자전거"
                ],
                "correct": 2,
                "explanation": "교차로에서는 보행자가 가장 우선순위가 높습니다."
            },
            "주차 및 정차": {
                "question": "다음 중 주차금지구역에 해당하지 않는 곳은?",
                "options": [
                    "교차로 모퉁이 5m 이내",
                    "횡단보도 10m 이내",
                    "버스정류장 10m 이내",
                    "주차장 출입구 3m 이내"
                ],
                "correct": 3,
                "explanation": "주차장 출입구는 3m 이내가 아닌 5m 이내가 주차금지구역입니다."
            },
            "고속도로": {
                "question": "고속도로에서 긴급상황으로 정차해야 할 때, 다음 중 올바른 행동은?",
                "options": [
                    "가능한 한 도로 우측에 정차한다",
                    "가능한 한 도로 좌측에 정차한다",
                    "가능한 한 도로 중앙에 정차한다",
                    "가능한 한 도로 밖으로 나간다"
                ],
                "correct": 0,
                "explanation": "고속도로에서는 가능한 한 도로 우측에 정차해야 합니다."
            },
            "특수상황": {
                "question": "어린이 보호구역에서 다음 중 올바른 운전 방법은?",
                "options": [
                    "시속 30km 이하로 주행한다",
                    "시속 50km 이하로 주행한다",
                    "시속 60km 이하로 주행한다",
                    "시속 80km 이하로 주행한다"
                ],
                "correct": 0,
                "explanation": "어린이 보호구역에서는 시속 30km 이하로 주행해야 합니다."
            }
        }
        
        return default_quizzes.get(category, default_quizzes["신호 및 표지"])
    
    def store_in_weaviate(self, quiz_data: Dict[str, Any], video_analysis: Dict[str, Any]):
        """퀴즈 데이터를 Weaviate에 저장"""
        try:
            # 퀴즈 텍스트 임베딩 생성
            quiz_text = f"{quiz_data['question']} {' '.join(quiz_data['options'])}"
            embedding = self.text_embedder.encode(quiz_text)
            
            # Weaviate에 데이터 저장
            data_object = {
                "question": quiz_data["question"],
                "options": quiz_data["options"],
                "correct_answer": quiz_data["correct"],
                "explanation": quiz_data["explanation"],
                "category": video_analysis["category"],
                "road_elements": video_analysis["road_elements"],
                "description": video_analysis["description"],
                "embedding": embedding.tolist()
            }
            
            self.weaviate_client.data_object.create(
                data_object=data_object,
                class_name="Quiz"
            )
            
        except Exception as e:
            print(f"Weaviate 저장 오류: {e}")
    
    def search_similar_quizzes(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """유사한 퀴즈 검색"""
        try:
            # 쿼리 임베딩 생성
            query_embedding = self.text_embedder.encode(query)
            
            # Weaviate에서 유사한 퀴즈 검색
            result = self.weaviate_client.query.get("Quiz", [
                "question", "options", "correct_answer", "explanation", "category"
            ]).with_near_vector({
                "vector": query_embedding.tolist()
            }).with_limit(limit).do()
            
            return result["data"]["Get"]["Quiz"]
            
        except Exception as e:
            print(f"유사 퀴즈 검색 오류: {e}")
            return []
    
    def create_quiz_from_video(self, video_path: str, category: str) -> Dict[str, Any]:
        """비디오에서 퀴즈 생성"""
        # 1. 비디오 분석
        road_elements = self.analyze_video_file(video_path)
        
        # 2. 상황 설명 생성
        description = self.generate_scenario_description(road_elements)
        
        # 3. 퀴즈 생성
        quiz = self.generate_quiz_from_description(description, category)
        
        # 4. Weaviate에 저장
        video_analysis = {
            "road_elements": road_elements,
            "description": description,
            "category": category
        }
        self.store_in_weaviate(quiz, video_analysis)
        
        return {
            "video_path": video_path,
            "road_elements": road_elements,
            "description": description,
            "quiz": quiz,
            "category": category
        } 