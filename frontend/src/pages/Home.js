import React from 'react';
import { Card, Row, Col, Statistic, Progress } from 'antd';
import { useAuth } from '../contexts/AuthContext';

const Home = () => {
  const { user } = useAuth();

  return (
    <div style={{ padding: '24px' }}>
      <h1>🏠 홈</h1>
      <p>안녕하세요, {user?.username || '사용자'}님!</p>
      
      <Row gutter={16} style={{ marginTop: '24px' }}>
        <Col span={8}>
          <Card>
            <Statistic
              title="총 퀴즈 수"
              value={25}
              suffix="개"
            />
          </Card>
        </Col>
        <Col span={8}>
          <Card>
            <Statistic
              title="정답률"
              value={85}
              suffix="%"
            />
          </Card>
        </Col>
        <Col span={8}>
          <Card>
            <Statistic
              title="현재 레벨"
              value="중급"
            />
          </Card>
        </Col>
      </Row>

      <Card title="📊 학습 진행도" style={{ marginTop: '24px' }}>
        <Progress percent={75} status="active" />
        <p>다음 레벨까지 25% 남았습니다!</p>
      </Card>

      <Row gutter={16} style={{ marginTop: '24px' }}>
        <Col span={12}>
          <Card title="🎯 오늘의 목표">
            <p>• 5개의 퀴즈 풀기</p>
            <p>• 오답노트 3개 복습</p>
            <p>• 새로운 카테고리 학습</p>
          </Card>
        </Col>
        <Col span={12}>
          <Card title="🏆 최근 성과">
            <p>• 연속 정답: 8개</p>
            <p>• 이번 주 퀴즈: 15개</p>
            <p>• 평균 정답률: 87%</p>
          </Card>
        </Col>
      </Row>
    </div>
  );
};

export default Home; 