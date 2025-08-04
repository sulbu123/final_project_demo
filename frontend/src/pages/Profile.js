import React, { useState } from 'react';
import { Card, Avatar, Button, Form, Input, message, Row, Col, Statistic } from 'antd';
import { UserOutlined, EditOutlined, SaveOutlined } from '@ant-design/icons';
import { useAuth } from '../contexts/AuthContext';

const Profile = () => {
  const { user, logout } = useAuth();
  const [isEditing, setIsEditing] = useState(false);
  const [form] = Form.useForm();

  const handleEdit = () => {
    setIsEditing(true);
    form.setFieldsValue({
      username: user?.username || '',
      email: user?.email || '',
    });
  };

  const handleSave = async (values) => {
    try {
      // TODO: 실제 API 호출로 변경
      message.success('프로필이 업데이트되었습니다!');
      setIsEditing(false);
    } catch (error) {
      message.error('프로필 업데이트에 실패했습니다.');
    }
  };

  const handleLogout = () => {
    logout();
    message.success('로그아웃되었습니다.');
  };

  return (
    <div style={{ padding: '24px' }}>
      <h1>👤 내정보</h1>

      <Row gutter={16}>
        <Col span={8}>
          <Card>
            <div style={{ textAlign: 'center' }}>
              <Avatar size={100} icon={<UserOutlined />} />
              <h2 style={{ marginTop: '16px' }}>{user?.username || '사용자'}</h2>
              <p>{user?.email || 'user@example.com'}</p>
              <Button 
                type="primary" 
                icon={<EditOutlined />}
                onClick={handleEdit}
                style={{ marginTop: '16px' }}
              >
                프로필 수정
              </Button>
            </div>
          </Card>
        </Col>

        <Col span={16}>
          <Card title="📊 내 통계">
            <Row gutter={16}>
              <Col span={8}>
                <Statistic
                  title="총 퀴즈"
                  value={149}
                  suffix="개"
                />
              </Col>
              <Col span={8}>
                <Statistic
                  title="정답률"
                  value={90}
                  suffix="%"
                  precision={1}
                />
              </Col>
              <Col span={8}>
                <Statistic
                  title="현재 레벨"
                  value="초급"
                />
              </Col>
            </Row>
          </Card>

          <Card title="⚙️ 계정 설정" style={{ marginTop: '16px' }}>
            <Form
              form={form}
              layout="vertical"
              onFinish={handleSave}
            >
              <Form.Item
                label="사용자명"
                name="username"
                rules={[{ required: true, message: '사용자명을 입력해주세요!' }]}
              >
                <Input disabled={!isEditing} />
              </Form.Item>

              <Form.Item
                label="이메일"
                name="email"
                rules={[
                  { required: true, message: '이메일을 입력해주세요!' },
                  { type: 'email', message: '올바른 이메일 형식이 아닙니다!' }
                ]}
              >
                <Input disabled={!isEditing} />
              </Form.Item>

              {isEditing && (
                <Form.Item>
                  <Button type="primary" htmlType="submit" icon={<SaveOutlined />}>
                    저장
                  </Button>
                  <Button 
                    style={{ marginLeft: '8px' }}
                    onClick={() => setIsEditing(false)}
                  >
                    취소
                  </Button>
                </Form.Item>
              )}
            </Form>
          </Card>

          <Card title="🔐 보안" style={{ marginTop: '16px' }}>
            <Button danger onClick={handleLogout}>
              로그아웃
            </Button>
          </Card>
        </Col>
      </Row>
    </div>
  );
};

export default Profile; 