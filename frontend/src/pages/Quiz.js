import React, { useState } from 'react';
import { Tabs, Upload, Select, Button, Card, Radio, message } from 'antd';
import { UploadOutlined, RobotOutlined, BookOutlined } from '@ant-design/icons';
import ReactPlayer from 'react-player';
import { useAuth } from '../contexts/AuthContext';
import { quizAPI } from '../services/api';
import styled from 'styled-components';

const { TabPane } = Tabs;
const { Dragger } = Upload;

const QuizContainer = styled.div`
  .ant-tabs-content {
    min-height: 500px;
  }
`;

const VideoPreview = styled.div`
  margin: 20px 0;
  text-align: center;
`;

const QuizCard = styled(Card)`
  margin: 20px 0;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
`;

const Quiz = () => {
  // eslint-disable-next-line no-unused-vars
  const { user } = useAuth();
  const [loading, setLoading] = useState(false);
  const [videoFile, setVideoFile] = useState(null);
  const [selectedCategory, setSelectedCategory] = useState('신호 및 표지');
  const [generatedQuiz, setGeneratedQuiz] = useState(null);
  const [selectedAnswer, setSelectedAnswer] = useState(null);
  const [showResult, setShowResult] = useState(false);
  const [existingQuiz, setExistingQuiz] = useState(null);
  const [selectedExistingCategory, setSelectedExistingCategory] = useState('신호 및 표지');

  const categories = [
    { value: '신호 및 표지', label: '신호 및 표지' },
    { value: '교차로 통과', label: '교차로 통과' },
    { value: '주차 및 정차', label: '주차 및 정차' },
    { value: '고속도로', label: '고속도로' },
    { value: '특수상황', label: '특수상황' },
  ];

  const handleVideoUpload = (info) => {
    const { file } = info;
    if (file.status === 'done') {
      setVideoFile(file);
      message.success(`${file.name} 파일이 업로드되었습니다.`);
    } else if (file.status === 'error') {
      message.error(`${file.name} 파일 업로드에 실패했습니다.`);
    }
  };

  const generateAIQuiz = async () => {
    if (!videoFile) {
      message.error('영상을 먼저 업로드해주세요.');
      return;
    }

    setLoading(true);
    try {
      const formData = new FormData();
      formData.append('video', videoFile.originFileObj);
      formData.append('category', selectedCategory);

      const response = await quizAPI.generateAIQuiz(videoFile.originFileObj, selectedCategory);
      setGeneratedQuiz(response.data);
      message.success('AI 퀴즈가 생성되었습니다!');
    } catch (error) {
      message.error('퀴즈 생성 중 오류가 발생했습니다.');
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  const submitAnswer = async () => {
    if (selectedAnswer === null) {
      message.error('답을 선택해주세요.');
      return;
    }

    try {
      const isCorrect = selectedAnswer === generatedQuiz.quiz.correct_answer;
      
      if (isCorrect) {
        message.success('✅ 정답입니다!');
      } else {
        message.error('❌ 틀렸습니다!');
      }

      // 결과를 서버에 저장
      await quizAPI.submitAnswer(generatedQuiz.quiz.id, selectedAnswer);

      setShowResult(true);
    } catch (error) {
      message.error('답변 제출 중 오류가 발생했습니다.');
    }
  };

  const startExistingQuiz = () => {
    // 임시 퀴즈 데이터 생성
    const tempQuiz = {
      id: 1,
      question: "교차로에서 우회전할 때 가장 안전한 방법은?",
      options: [
        "빨리 우회전하기",
        "왼쪽을 확인하고 천천히 우회전하기", 
        "신호등만 보고 우회전하기",
        "다른 차량이 없으면 무시하고 우회전하기"
      ],
      correct_answer: 1,
      explanation: "우회전 시에는 반드시 왼쪽을 확인하고 천천히 우회전해야 합니다. 특히 보행자와 자전거를 주의해야 합니다.",
      category: selectedExistingCategory
    };
    
    setExistingQuiz(tempQuiz);
    setSelectedAnswer(null);
    setShowResult(false);
    message.success('퀴즈가 시작되었습니다!');
  };

  const renderAIQuizTab = () => (
    <div>
      <h2>🎬 영상 업로드 및 AI 퀴즈 생성</h2>
      <p>도로 주행 영상을 업로드하면 AI가 분석하여 맞춤형 퀴즈를 생성합니다.</p>
      
      <Card title="영상 업로드" style={{ marginBottom: 20 }}>
        <Dragger
          name="video"
          multiple={false}
          accept="video/*"
          onChange={handleVideoUpload}
          beforeUpload={() => false}
        >
          <p className="ant-upload-drag-icon">
            <UploadOutlined />
          </p>
          <p className="ant-upload-text">클릭하거나 파일을 드래그하여 업로드하세요</p>
          <p className="ant-upload-hint">MP4, AVI, MOV 파일을 지원합니다</p>
        </Dragger>
      </Card>

      {videoFile && (
        <VideoPreview>
          <h3>업로드된 영상</h3>
          <ReactPlayer
            url={URL.createObjectURL(videoFile.originFileObj)}
            controls
            width="100%"
            height="300px"
          />
        </VideoPreview>
      )}

      <Card title="퀴즈 설정" style={{ marginBottom: 20 }}>
        <div style={{ marginBottom: 16 }}>
          <label>카테고리 선택:</label>
          <Select
            style={{ width: '100%', marginTop: 8 }}
            value={selectedCategory}
            onChange={setSelectedCategory}
            options={categories}
          />
        </div>
        
        <Button
          type="primary"
          icon={<RobotOutlined />}
          size="large"
          onClick={generateAIQuiz}
          loading={loading}
          disabled={!videoFile}
        >
          🤖 AI 퀴즈 생성
        </Button>
      </Card>

      {generatedQuiz && (
        <QuizCard title="📝 생성된 퀴즈">
          <h3>{generatedQuiz.quiz.question}</h3>
          
          <Radio.Group
            onChange={(e) => setSelectedAnswer(e.target.value)}
            value={selectedAnswer}
            style={{ width: '100%' }}
          >
            {generatedQuiz.quiz.options.map((option, index) => (
              <Radio key={index} value={index} style={{ display: 'block', marginBottom: 12 }}>
                {option}
              </Radio>
            ))}
          </Radio.Group>

          <div style={{ marginTop: 20 }}>
            <Button type="primary" onClick={submitAnswer} disabled={selectedAnswer === null}>
              답변 제출
            </Button>
          </div>

          {showResult && (
            <div style={{ marginTop: 20, padding: 16, backgroundColor: '#f6ffed', borderRadius: 6 }}>
              <h4>해설:</h4>
              <p>{generatedQuiz.quiz.explanation}</p>
            </div>
          )}
        </QuizCard>
      )}
    </div>
  );

  const renderExistingQuizTab = () => (
    <div>
      <h2>📚 기존 퀴즈 풀기</h2>
      <p>카테고리별로 준비된 퀴즈를 풀어보세요.</p>
      
      <Card title="퀴즈 선택">
        <div style={{ marginBottom: 16 }}>
          <label>카테고리 선택:</label>
          <Select
            style={{ width: '100%', marginTop: 8 }}
            placeholder="카테고리를 선택하세요"
            value={selectedExistingCategory}
            onChange={setSelectedExistingCategory}
            options={categories}
          />
        </div>
        
        <Button 
          type="primary" 
          icon={<BookOutlined />}
          onClick={startExistingQuiz}
        >
          퀴즈 시작
        </Button>
      </Card>

      {existingQuiz && (
        <QuizCard title={`📝 ${existingQuiz.category} 퀴즈`}>
          <h3>{existingQuiz.question}</h3>
          
          <Radio.Group
            onChange={(e) => setSelectedAnswer(e.target.value)}
            value={selectedAnswer}
            style={{ width: '100%' }}
          >
            {existingQuiz.options.map((option, index) => (
              <Radio key={index} value={index} style={{ display: 'block', marginBottom: 12 }}>
                {option}
              </Radio>
            ))}
          </Radio.Group>

          <div style={{ marginTop: 20 }}>
            <Button 
              type="primary" 
              onClick={() => {
                if (selectedAnswer === existingQuiz.correct_answer) {
                  message.success('✅ 정답입니다!');
                } else {
                  message.error('❌ 틀렸습니다!');
                }
                setShowResult(true);
              }} 
              disabled={selectedAnswer === null}
            >
              답변 제출
            </Button>
          </div>

          {showResult && (
            <div style={{ marginTop: 20, padding: 16, backgroundColor: '#f6ffed', borderRadius: 6 }}>
              <h4>해설:</h4>
              <p>{existingQuiz.explanation}</p>
            </div>
          )}
        </QuizCard>
      )}
    </div>
  );

  return (
    <QuizContainer>
      <Tabs defaultActiveKey="ai" size="large">
        <TabPane
          tab={
            <span>
              <RobotOutlined />
              AI 퀴즈 생성
            </span>
          }
          key="ai"
        >
          {renderAIQuizTab()}
        </TabPane>
        <TabPane
          tab={
            <span>
              <BookOutlined />
              기존 퀴즈
            </span>
          }
          key="existing"
        >
          {renderExistingQuizTab()}
        </TabPane>
      </Tabs>
    </QuizContainer>
  );
};

export default Quiz; 