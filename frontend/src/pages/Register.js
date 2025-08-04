import React from 'react';
import { Form, Input, Button, Card, message } from 'antd';
import { UserOutlined, LockOutlined, MailOutlined } from '@ant-design/icons';
import { useAuth } from '../contexts/AuthContext';
import { useNavigate } from 'react-router-dom';

const Register = () => {
  const { register } = useAuth();
  const navigate = useNavigate();

  const onFinish = async (values) => {
    try {
      const result = await register(values.email, values.username, values.password);
      if (result.success) {
        message.success('회원가입 성공!');
        navigate('/');
      } else {
        message.error(result.error || '회원가입에 실패했습니다.');
      }
    } catch (error) {
      message.error('회원가입 중 오류가 발생했습니다.');
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
      <Card style={{ width: 400 }}>
        <div style={{ textAlign: 'center', marginBottom: '24px' }}>
          <h1>🚗 도로 주행 퀴즈</h1>
          <p>회원가입하여 학습을 시작하세요!</p>
        </div>

        <Form
          name="register"
          onFinish={onFinish}
          autoComplete="off"
        >
          <Form.Item
            name="username"
            rules={[{ required: true, message: '사용자명을 입력해주세요!' }]}
          >
            <Input 
              prefix={<UserOutlined />} 
              placeholder="사용자명" 
              size="large"
            />
          </Form.Item>

          <Form.Item
            name="email"
            rules={[
              { required: true, message: '이메일을 입력해주세요!' },
              { type: 'email', message: '올바른 이메일 형식이 아닙니다!' }
            ]}
          >
            <Input 
              prefix={<MailOutlined />} 
              placeholder="이메일" 
              size="large"
            />
          </Form.Item>

          <Form.Item
            name="password"
            rules={[
              { required: true, message: '비밀번호를 입력해주세요!' },
              { min: 6, message: '비밀번호는 최소 6자 이상이어야 합니다!' }
            ]}
          >
            <Input.Password
              prefix={<LockOutlined />}
              placeholder="비밀번호"
              size="large"
            />
          </Form.Item>

          <Form.Item
            name="confirmPassword"
            dependencies={['password']}
            rules={[
              { required: true, message: '비밀번호를 다시 입력해주세요!' },
              ({ getFieldValue }) => ({
                validator(_, value) {
                  if (!value || getFieldValue('password') === value) {
                    return Promise.resolve();
                  }
                  return Promise.reject(new Error('비밀번호가 일치하지 않습니다!'));
                },
              }),
            ]}
          >
            <Input.Password
              prefix={<LockOutlined />}
              placeholder="비밀번호 확인"
              size="large"
            />
          </Form.Item>

          <Form.Item>
            <Button type="primary" htmlType="submit" size="large" block>
              회원가입
            </Button>
          </Form.Item>

          <div style={{ textAlign: 'center' }}>
            <p>이미 계정이 있으신가요? <a href="/login">로그인</a></p>
          </div>
        </Form>
      </Card>
    </div>
  );
};

export default Register; 