import React, { useState } from 'react';
import {
  Container,
  Paper,
  TextField,
  Button,
  Typography,
  Box,
  Alert,
  CircularProgress,
  Link,
  Divider,
} from '@mui/material';
import { useAuth } from '../contexts/AuthContext';

interface LoginFormProps {
  onSwitchToSignup: () => void;
  onForgotPassword: () => void;
  onLoginError?: (hasError: boolean) => void;
}

const LoginForm: React.FC<LoginFormProps> = ({ onSwitchToSignup, onForgotPassword, onLoginError }) => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState<string | null>(null);
  
  // Test: Force error display for debugging
  const [forceError, setForceError] = useState<string | null>(null);
  const [showLoginError, setShowLoginError] = useState(false);
  
  // Debug: Track error state changes
  const setErrorWithLog = (newError: string | null) => {
    console.log('setError called with:', newError);
    console.trace('Stack trace for setError');
    setError(newError);
  };
  const [isLoading, setIsLoading] = useState(false);
  const { login } = useAuth();

  const handleSubmit = async (e: React.FormEvent) => {
    console.log('Form submit triggered');
    e.preventDefault();
    console.log('preventDefault called');
    setErrorWithLog(null);
    setForceError(null); // Clear force error on new submit
    setShowLoginError(false); // Clear login error flag
    localStorage.removeItem('loginError'); // Clear localStorage error

    if (!email || !password) {
      setErrorWithLog('Please fill in all fields');
      return;
    }

    if (!email.includes('@')) {
      setErrorWithLog('Please enter a valid email address');
      return;
    }

    setIsLoading(true);
    
    try {
      await login({ email, password });
      // Navigation will be handled by App.tsx based on auth state
    } catch (err) {
      console.log('Full error object:', err);
      console.log('Error type:', typeof err);
      console.log('Error message:', err instanceof Error ? err.message : 'Not an Error object');
      
      const errorMessage = err instanceof Error ? err.message : 'Login failed';
      
      // Simple unified error message for any login failure
      console.log('Login failed with:', errorMessage);
      setErrorWithLog('LOGIN_FAILED');
      // Force error to persist
      console.log('Setting forceError to LOGIN_FAILED');
      setForceError('LOGIN_FAILED');
      setShowLoginError(true);
      localStorage.setItem('loginError', 'true');
      console.log('Set showLoginError to true and localStorage loginError');
    } finally {
      setIsLoading(false);
    }
  };

  console.log('LoginForm render - current error state:', error);
  console.log('LoginForm render - forceError state:', forceError);
  console.log('LoginForm render - showLoginError state:', showLoginError);
  
  return (
    <Container maxWidth="sm" sx={{ py: 8 }}>
      <Paper elevation={3} sx={{ p: 4 }}>
        <Box sx={{ textAlign: 'center', mb: 4 }}>
          <img 
            src="/knowledgecore.jpeg" 
            alt="Knowledge Core Logo" 
            style={{ height: '60px', marginBottom: '20px' }}
          />
          <Typography variant="h4" component="h1" gutterBottom>
            Sign In
          </Typography>
          <Typography variant="body1" color="text.secondary">
            Welcome back to Knowledge Core IQ Search
          </Typography>
        </Box>

        <form onSubmit={handleSubmit}>
          <TextField
            fullWidth
            label="Email Address"
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            margin="normal"
            required
            autoFocus
            autoComplete="email"
          />
          
          <TextField
            fullWidth
            label="Password"
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            margin="normal"
            required
            autoComplete="current-password"
          />



          {(error || forceError || showLoginError || localStorage.getItem('loginError') === 'true') && (
            <Alert 
              severity="info" 
              sx={{ 
                mt: 2,
                backgroundColor: '#f5f5f5',
                color: '#333',
                border: '1px solid #ddd',
                '& .MuiAlert-icon': {
                  color: '#666'
                }
              }}
              action={
                (() => {
                  console.log('Rendering error alert with error:', error || forceError);
                  return (error === 'LOGIN_FAILED' || forceError === 'LOGIN_FAILED' || showLoginError || localStorage.getItem('loginError') === 'true') ? (
                    <Button 
                      variant="outlined"
                      size="small" 
                      onClick={onForgotPassword}
                      sx={{ 
                        whiteSpace: 'nowrap',
                        borderColor: 'primary.main',
                        color: 'primary.main',
                        fontWeight: 600,
                        textTransform: 'none',
                        px: 2,
                        py: 0.5,
                        '&:hover': {
                          backgroundColor: 'primary.main',
                          color: 'white',
                          borderColor: 'primary.main',
                        }
                      }}
                    >
                      Reset Password
                    </Button>
                  ) : null;
                })()
              }
            >
              'Incorrect details. Do you want to try forgotten password?'
            </Alert>
          )}

          <Button
            type="submit"
            fullWidth
            variant="contained"
            size="large"
            disabled={isLoading}
            sx={{ 
              mt: 3, 
              mb: 2, 
              py: 1.5,
              backgroundColor: '#283E56',
              '&:hover': {
                backgroundColor: '#1e2f42'
              },
              '&:disabled': {
                backgroundColor: '#666'
              }
            }}
          >
            {isLoading ? <CircularProgress size={24} /> : 'Sign In'}
          </Button>

          <Divider sx={{ my: 2 }} />

          <Box sx={{ textAlign: 'center' }}>
            <Typography variant="body2">
              Don't have an account?{' '}
              <Link
                component="button"
                type="button"
                onClick={onSwitchToSignup}
                sx={{ cursor: 'pointer' }}
              >
                Sign up here
              </Link>
            </Typography>
          </Box>
        </form>
      </Paper>
    </Container>
  );
};

export default LoginForm;