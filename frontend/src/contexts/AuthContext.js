import React, { createContext, useContext, useState } from 'react';

const AuthContext = createContext();
const API_BASE_URL = 'http://localhost:8000';

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(false);

  const login = async (email, password) => {
    setLoading(true);
    try {
      const formData = new FormData();
      formData.append('username', email);
      formData.append('password', password);
      
      console.log('Attempting login...', email);

      const response = await fetch(`${API_BASE_URL}/api/auth/login`, {
        method: 'POST',
        body: formData,
        headers: {
          'Accept': 'application/json',
        }
      });
      
      console.log('Login response:', response);

      if (response.ok) {
        const data = await response.json();
        localStorage.setItem('token', data.access_token);
        
        // 사용자 정보 가져오기
        const userResponse = await fetch(`${API_BASE_URL}/api/auth/me`, {
          headers: {
            'Authorization': `Bearer ${data.access_token}`,
            'Accept': 'application/json',
          }
        });
        
        if (userResponse.ok) {
          const userData = await userResponse.json();
          setUser(userData);
          return { success: true };
        }
      }
      
      const errorData = await response.json().catch(() => ({ detail: '로그인에 실패했습니다.' }));
      return { success: false, error: errorData.detail || '로그인에 실패했습니다.' };
    } catch (error) {
      console.error('Login error:', error);
      return { success: false, error: '서버에 연결할 수 없습니다.' };
    } finally {
      setLoading(false);
    }
  };

  const register = async (email, username, password) => {
    setLoading(true);
    try {
      console.log('Attempting registration...', { email, username });

      console.log('Registration payload:', { email, username, password });
      const response = await fetch(`${API_BASE_URL}/api/auth/register`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
        },
        mode: 'cors',
        credentials: 'include',
        body: JSON.stringify({
          email,
          username,
          password
        }),
      });
      
      console.log('Registration response:', response);

      if (response.ok) {
        const userData = await response.json();
        // 회원가입 성공 후 자동 로그인
        const loginResult = await login(email, password);
        if (loginResult.success) {
          return { success: true, data: userData };
        } else {
          return { success: false, error: '회원가입은 성공했지만 자동 로그인에 실패했습니다.' };
        }
      } else {
        const errorData = await response.json();
        return { success: false, error: errorData.detail || '회원가입에 실패했습니다.' };
      }
    } catch (error) {
      console.error('Registration error:', error);
      return { success: false, error: '서버에 연결할 수 없습니다.' };
    } finally {
      setLoading(false);
    }
  };

  const logout = () => {
    setUser(null);
    localStorage.removeItem('token');
  };

  const value = {
    user,
    loading,
    login,
    logout,
    register
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};