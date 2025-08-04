import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { ConfigProvider } from 'antd';
import koKR from 'antd/locale/ko_KR';
import { AuthProvider } from './contexts/AuthContext';
import Layout from './components/Layout';
import Home from './pages/Home';
import Quiz from './pages/Quiz';
import WrongAnswers from './pages/WrongAnswers';
import Analysis from './pages/Analysis';
import Profile from './pages/Profile';
import Login from './pages/Login';
import Register from './pages/Register';
import ProtectedRoute from './components/ProtectedRoute';
import './App.css';

function App() {
  return (
    <ConfigProvider locale={koKR}>
      <AuthProvider>
        <Router>
          <div className="App">
            <Routes>
              {/* 공개 라우트 */}
              <Route path="/login" element={<Login />} />
              <Route path="/register" element={<Register />} />
              
              {/* 보호된 라우트 */}
              <Route
                path="/"
                element={
                  <ProtectedRoute>
                    <Layout />
                  </ProtectedRoute>
                }
              >
                <Route index element={<Home />} />
                <Route path="quiz" element={<Quiz />} />
                <Route path="wrong-answers" element={<WrongAnswers />} />
                <Route path="analysis" element={<Analysis />} />
                <Route path="profile" element={<Profile />} />
              </Route>

              {/* 기본 리다이렉트 */}
              <Route path="*" element={<Navigate to="/login" replace />} />
            </Routes>
          </div>
        </Router>
      </AuthProvider>
    </ConfigProvider>
  );
}

export default App; 