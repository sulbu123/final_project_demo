import React, { useState } from 'react';
import { List, Tag, Button, Modal, message } from 'antd';
import { useAuth } from '../contexts/AuthContext';

const WrongAnswers = () => {
  // eslint-disable-next-line no-unused-vars
  const { user } = useAuth();
  const [selectedQuiz, setSelectedQuiz] = useState(null);
  const [isModalVisible, setIsModalVisible] = useState(false);

  // 임시 데이터
  const wrongAnswers = [
    {
      id: 1,
      question: "교차로에서 우회전할 때 가장 안전한 방법은?",
      userAnswer: "빨리 우회전하기",
      correctAnswer: "왼쪽을 확인하고 천천히 우회전하기",
      explanation: "우회전 시에는 반드시 왼쪽을 확인하고 천천히 우회전해야 합니다.",
      category: "교차로",
      date: "2024-01-15"
    },
    {
      id: 2,
      question: "비상등을 켜야 하는 상황은?",
      userAnswer: "항상 켜두기",
      correctAnswer: "차량 고장이나 사고 시에만",
      explanation: "비상등은 차량 고장이나 사고 시에만 사용해야 합니다.",
      category: "안전운전",
      date: "2024-01-14"
    }
  ];

  const showModal = (quiz) => {
    setSelectedQuiz(quiz);
    setIsModalVisible(true);
  };

  const handleReview = () => {
    message.success('복습 완료!');
    setIsModalVisible(false);
  };

  return (
    <div style={{ padding: '24px' }}>
      <h1>❌ 오답노트</h1>
      <p>틀린 문제들을 복습해보세요!</p>

      <List
        itemLayout="vertical"
        size="large"
        pagination={{
          onChange: (page) => {
            console.log(page);
          },
          pageSize: 10,
        }}
        dataSource={wrongAnswers}
        renderItem={(item) => (
          <List.Item
            key={item.id}
            actions={[
              <Button type="primary" onClick={() => showModal(item)}>
                복습하기
              </Button>
            ]}
            extra={
              <div>
                <Tag color="red">{item.category}</Tag>
                <br />
                <small>{item.date}</small>
              </div>
            }
          >
            <List.Item.Meta
              title={item.question}
              description={
                <div>
                  <p><strong>내 답변:</strong> {item.userAnswer}</p>
                  <p><strong>정답:</strong> {item.correctAnswer}</p>
                </div>
              }
            />
          </List.Item>
        )}
      />

      <Modal
        title="문제 복습"
        visible={isModalVisible}
        onOk={handleReview}
        onCancel={() => setIsModalVisible(false)}
        okText="복습 완료"
        cancelText="닫기"
      >
        {selectedQuiz && (
          <div>
            <h3>{selectedQuiz.question}</h3>
            <p><strong>내 답변:</strong> {selectedQuiz.userAnswer}</p>
            <p><strong>정답:</strong> {selectedQuiz.correctAnswer}</p>
            <p><strong>설명:</strong> {selectedQuiz.explanation}</p>
          </div>
        )}
      </Modal>
    </div>
  );
};

export default WrongAnswers; 