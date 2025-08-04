import React, { useEffect } from 'react';
import { Form, Input, Button, Card, message } from 'antd';
import { UserOutlined, LockOutlined } from '@ant-design/icons';
import { useAuth } from '../contexts/AuthContext';
import { useNavigate } from 'react-router-dom';
import useIsMobile from '../hooks/useIsMobile';
import styled from 'styled-components';

const StyledCard = styled(Card)`
  width: ${props => props.isMobile ? '90%' : '400px'};
  margin: ${props => props.isMobile ? '20px' : '0'};
`;

const Login = () => {
  const { login, user } = useAuth();
  const navigate = useNavigate();
  const isMobile = useIsMobile();


  useEffect(() => {
    // 이미 로그인된 경우 홈으로 리다이렉트
    if (user) {
      navigate('/');
    }
  }, [user, navigate]);

  const onFinish = async (values) => {
    try {
      const result = await login(values.email, values.password);
      if (result.success) {
        message.success('로그인 성공!');
        navigate('/');
      } else {
        message.error(result.error || '로그인에 실패했습니다.');
      }
    } catch (error) {
      message.error('로그인 중 오류가 발생했습니다.');
    }
  };

  return (
    <div style={{ 
      display: 'flex', 
      justifyContent: 'center', 
      alignItems: 'center', 
      minHeight: '100vh',
      background: '#f0f2f5'
    }}>
      <StyledCard isMobile={isMobile}>
        <div style={{ textAlign: 'center', marginBottom: '24px' }}>
          <h1 style={{ fontSize: isMobile ? '24px' : '28px' }}>🚗 도로 주행 퀴즈</h1>
          <p>로그인하여 학습을 시작하세요!</p>
        </div>

        <Form
          name="login"
          onFinish={onFinish}
          autoComplete="off"
        >
          <Form.Item
            name="email"
            rules={[
              { required: true, message: '이메일을 입력해주세요!' },
              { type: 'email', message: '올바른 이메일 형식이 아닙니다!' }
            ]}
          >
            <Input 
              prefix={<UserOutlined />} 
              placeholder="이메일" 
              size="large"
            />
          </Form.Item>

          <Form.Item
            name="password"
            rules={[{ required: true, message: '비밀번호를 입력해주세요!' }]}
          >
            <Input.Password
              prefix={<LockOutlined />}
              placeholder="비밀번호"
              size="large"
            />
          </Form.Item>

          <Form.Item>
            <Button type="primary" htmlType="submit" size="large" block>
              로그인
            </Button>
          </Form.Item>

          <div style={{ textAlign: 'center' }}>
            <p>계정이 없으신가요? <a href="/register">회원가입</a></p>
          </div>
        </Form>
      </StyledCard>
    </div>
  );
};

export default Login; 