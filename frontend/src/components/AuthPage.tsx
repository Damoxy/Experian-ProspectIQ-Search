import React, { useState } from 'react';
import { Box } from '@mui/material';
import LoginForm from './LoginForm';
import SignupForm from './SignupForm';
import ForgotPassword from './ForgotPassword';

type AuthView = 'login' | 'signup' | 'forgot-password';

const AuthPage: React.FC = () => {
  const [currentView, setCurrentView] = useState<AuthView>('login');

  const renderCurrentView = () => {
    switch (currentView) {
      case 'login':
        return (
          <LoginForm 
            onSwitchToSignup={() => setCurrentView('signup')}
            onForgotPassword={() => setCurrentView('forgot-password')}
          />
        );
      case 'signup':
        return (
          <SignupForm onSwitchToLogin={() => setCurrentView('login')} />
        );
      case 'forgot-password':
        return (
          <ForgotPassword onBackToLogin={() => setCurrentView('login')} />
        );
      default:
        return (
          <LoginForm 
            onSwitchToSignup={() => setCurrentView('signup')}
            onForgotPassword={() => setCurrentView('forgot-password')}
          />
        );
    }
  };

  return (
    <Box 
      sx={{ 
        position: 'relative', 
        minHeight: '100vh', 
        overflow: 'hidden',
        background: '#283E56',
      }}
    >
      <Box sx={{ position: 'relative', zIndex: 1 }}>
        {renderCurrentView()}
      </Box>
    </Box>
  );
};

export default AuthPage;