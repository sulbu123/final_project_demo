import React from 'react';
import { Navigate, useLocation } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';

const ProtectedRoute = ({ children }) => {
  const { user } = useAuth();
  const location = useLocation();

  if (!user) {
    // 로그인되지 않은 경우 로그인 페이지로 리다이렉트
    return <Navigate to="/login" state={{ from: location }} replace />;
  }

  return children;
};

export default ProtectedRoute;