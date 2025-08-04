import React from 'react';
import { Card, Row, Col, Progress, Statistic } from 'antd';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

const Analysis = () => {
  // 임시 데이터
  const progressData = [
    { date: '1월', score: 65 },
    { date: '2월', score: 70 },
    { date: '3월', score: 75 },
    { date: '4월', score: 80 },
    { date: '5월', score: 85 },
    { date: '6월', score: 90 },
  ];

  const categoryData = [
    { name: '교차로', value: 30 },
    { name: '안전운전', value: 25 },
    { name: '신호등', value: 20 },
    { name: '주차', value: 15 },
    { name: '기타', value: 10 },
  ];

  return (
    <div style={{ padding: '24px' }}>
      <h1>📊 학습분석</h1>
      <p>나의 학습 현황을 확인해보세요!</p>

      <Row gutter={16} style={{ marginTop: '24px' }}>
        <Col span={8}>
          <Card>
            <Statistic
              title="총 퀴즈 수"
              value={150}
              suffix="개"
            />
          </Card>
        </Col>
        <Col span={8}>
          <Card>
            <Statistic
              title="평균 정답률"
              value={87.5}
              suffix="%"
              precision={1}
            />
          </Card>
        </Col>
        <Col span={8}>
          <Card>
            <Statistic
              title="학습 일수"
              value={45}
              suffix="일"
            />
          </Card>
        </Col>
      </Row>

      <Row gutter={16} style={{ marginTop: '24px' }}>
        <Col span={12}>
          <Card title="📈 점수 변화">
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={progressData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="date" />
                <YAxis />
                <Tooltip />
                <Line type="monotone" dataKey="score" stroke="#8884d8" strokeWidth={2} />
              </LineChart>
            </ResponsiveContainer>
          </Card>
        </Col>
        <Col span={12}>
          <Card title="📋 카테고리별 성과">
            {categoryData.map((item, index) => (
              <div key={index} style={{ marginBottom: '16px' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '8px' }}>
                  <span>{item.name}</span>
                  <span>{item.value}%</span>
                </div>
                <Progress percent={item.value} size="small" />
              </div>
            ))}
          </Card>
        </Col>
      </Row>

      <Row gutter={16} style={{ marginTop: '24px' }}>
        <Col span={12}>
          <Card title="🎯 학습 목표">
            <p>• 이번 달 목표: 200개 퀴즈 풀기</p>
            <Progress percent={75} />
            <p>• 평균 정답률 90% 달성</p>
            <Progress percent={87.5} />
            <p>• 모든 카테고리 완료</p>
            <Progress percent={60} />
          </Card>
        </Col>
        <Col span={12}>
          <Card title="🏆 성취도">
            <p>• 연속 정답: 15개</p>
            <p>• 최고 점수: 95점</p>
            <p>• 학습 시간: 120시간</p>
            <p>• 완료한 퀴즈: 150개</p>
          </Card>
        </Col>
      </Row>
    </div>
  );
};

export default Analysis; 