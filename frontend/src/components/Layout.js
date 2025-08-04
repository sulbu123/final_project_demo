import React, { useState } from 'react';
import { Layout as AntLayout, Menu, Avatar, Dropdown, Button, Drawer } from 'antd';
import { Outlet, useNavigate, useLocation } from 'react-router-dom';
import {
  HomeOutlined,
  BookOutlined,
  FileTextOutlined,
  BarChartOutlined,
  UserOutlined,
  LogoutOutlined,
  MenuOutlined
} from '@ant-design/icons';
import { useAuth } from '../contexts/AuthContext';
import styled from 'styled-components';
import useIsMobile from '../hooks/useIsMobile';

const { Header, Sider, Content } = AntLayout;

const StyledLayout = styled(AntLayout)`
  min-height: 100vh;
`;

const StyledHeader = styled(Header)`
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: #fff;
  padding: 0 24px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
`;

const Logo = styled.div`
  font-size: 20px;
  font-weight: bold;
  color: #1890ff;
`;

const UserInfo = styled.div`
  display: flex;
  align-items: center;
  gap: 8px;
`;

const StyledContent = styled(Content)`
  margin: 24px;
  padding: 24px;
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
`;

const Layout = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const { user, logout } = useAuth();
  const isMobile = useIsMobile();
  const [drawerVisible, setDrawerVisible] = useState(false);

  const menuItems = [
    {
      key: '/',
      icon: <HomeOutlined />,
      label: '홈',
    },
    {
      key: '/quiz',
      icon: <BookOutlined />,
      label: '퀴즈풀기',
    },
    {
      key: '/wrong-answers',
      icon: <FileTextOutlined />,
      label: '오답노트',
    },
    {
      key: '/analysis',
      icon: <BarChartOutlined />,
      label: '학습분석',
    },
    {
      key: '/profile',
      icon: <UserOutlined />,
      label: '내정보',
    },
  ];

  const userMenuItems = [
    {
      key: 'profile',
      icon: <UserOutlined />,
      label: '프로필',
    },
    {
      key: 'logout',
      icon: <LogoutOutlined />,
      label: '로그아웃',
      onClick: () => {
        logout();
        navigate('/login');
      },
    },
  ];

  const handleMenuClick = ({ key }) => {
    navigate(key);
  };

  return (
    <StyledLayout>
      {!isMobile && (
        <Sider
          width={250}
          style={{
            background: '#fff',
            boxShadow: '2px 0 8px rgba(0, 0, 0, 0.1)',
          }}
        >
          <div style={{ padding: '24px', textAlign: 'center' }}>
            <Logo>🚗 도로 주행 퀴즈</Logo>
          </div>
          <Menu
            mode="inline"
            selectedKeys={[location.pathname]}
            items={menuItems}
            onClick={handleMenuClick}
            style={{ borderRight: 0 }}
          />
        </Sider>
      )}
      <AntLayout>
        <StyledHeader>
          {isMobile ? (
            <>
              <Button
                type="text"
                icon={<MenuOutlined />}
                onClick={() => setDrawerVisible(true)}
              />
              <Logo style={{ margin: '0 auto' }}>🚗 도로 주행 퀴즈</Logo>
            </>
          ) : (
            <div />
          )}
          <UserInfo>
            <Avatar icon={<UserOutlined />} />
            <Dropdown
              menu={{ items: userMenuItems }}
              placement="bottomRight"
            >
              <span style={{ cursor: 'pointer' }}>
                {user?.username || '사용자'}
              </span>
            </Dropdown>
          </UserInfo>
        </StyledHeader>
        <StyledContent>
          <Outlet />
        </StyledContent>
      </AntLayout>

      {/* 모바일 메뉴 드로어 */}
      <Drawer
        title="메뉴"
        placement="left"
        onClose={() => setDrawerVisible(false)}
        visible={drawerVisible}
      >
        <Menu
          mode="vertical"
          selectedKeys={[location.pathname]}
          items={menuItems}
          onClick={(item) => {
            handleMenuClick(item);
            setDrawerVisible(false);
          }}
        />
      </Drawer>
    </StyledLayout>
  );
};

export default Layout; 