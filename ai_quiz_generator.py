import cv2
import numpy as np
from PIL import Image
import torch
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
import openai
import os
from dotenv import load_dotenv
import json
import random

# 환경 변수 로드
load_dotenv()

class AIQuizGenerator:
    def __init__(self):
        """AI 퀴즈 생성기 초기화"""
        self.openai_client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        
        # 이미지 분석을 위한 모델 (실제로는 더 정교한 모델 사용)
        self.image_analyzer = pipeline("image-classification", model="microsoft/resnet-50")
        
        # 텍스트 생성 모델
        self.text_generator = pipeline("text-generation", model="gpt2")
        
        # 도로교통법 관련 키워드
        self.traffic_keywords = {
            "신호등": ["빨간불", "초록불", "노란불", "좌회전", "우회전", "직진"],
            "교차로": ["우선순위", "보행자", "차량", "신호등", "정지선"],
            "주차": ["주차금지", "정차", "주차장", "출입구", "거리"],
            "고속도로": ["진입", "진출", "속도제한", "차선변경", "정차"],
            "특수상황": ["긴급차량", "장애인", "어린이", "보호구역", "학교"]
        }
    
    def analyze_video_frame(self, frame):
        """비디오 프레임 분석"""
        try:
            # 프레임을 PIL 이미지로 변환
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            pil_image = Image.fromarray(frame_rgb)
            
            # 이미지 분석
            results = self.image_analyzer(pil_image)
            
            # 분석 결과에서 도로 관련 요소 추출
            road_elements = []
            for result in results:
                if any(keyword in result['label'].lower() for keyword in ['car', 'road', 'traffic', 'signal', 'crossing']):
                    road_elements.append(result['label'])
            
            return road_elements
        except Exception as e:
            print(f"프레임 분석 오류: {e}")
            return []
    
    def generate_scenario_description(self, road_elements):
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
    
    def generate_quiz_from_description(self, description, category):
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
                # JSON 파싱 실패 시 기본 퀴즈 생성
                return self.generate_default_quiz(category)
                
        except Exception as e:
            print(f"퀴즈 생성 오류: {e}")
            return self.generate_default_quiz(category)
    
    def generate_default_quiz(self, category):
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
    
    def analyze_video_file(self, video_path):
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
    
    def create_quiz_from_video(self, video_path, category):
        """비디오에서 퀴즈 생성"""
        # 1. 비디오 분석
        road_elements = self.analyze_video_file(video_path)
        
        # 2. 상황 설명 생성
        description = self.generate_scenario_description(road_elements)
        
        # 3. 퀴즈 생성
        quiz = self.generate_quiz_from_description(description, category)
        
        return {
            "video_path": video_path,
            "road_elements": road_elements,
            "description": description,
            "quiz": quiz,
            "category": category
        }

# 사용 예시
if __name__ == "__main__":
    generator = AIQuizGenerator()
    
    # 샘플 비디오 파일이 있다면
    # result = generator.create_quiz_from_video("sample_video.mp4", "신호 및 표지")
    # print(result) 