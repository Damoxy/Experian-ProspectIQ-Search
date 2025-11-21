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
import { ArrowBack, Email } from '@mui/icons-material';
import { authAPI } from '../services/api';

interface ForgotPasswordProps {
  onBackToLogin: () => void;
}

const ForgotPassword: React.FC<ForgotPasswordProps> = ({ onBackToLogin }) => {
  const [email, setEmail] = useState('');
  const [newPassword, setNewPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [message, setMessage] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [isSuccess, setIsSuccess] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setMessage(null);

    if (!email) {
      setError('Please enter your email address');
      return;
    }

    if (!email.includes('@')) {
      setError('Please enter a valid email address');
      return;
    }

    if (!newPassword) {
      setError('Please enter a new password');
      return;
    }

    if (newPassword.length < 6) {
      setError('Password must be at least 6 characters long');
      return;
    }

    if (newPassword !== confirmPassword) {
      setError('Passwords do not match');
      return;
    }

    setIsLoading(true);

    try {
      const response = await authAPI.resetPassword('', newPassword, email);
      setIsSuccess(true);
      setMessage(response.message);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred. Please try again later.');
    } finally {
      setIsLoading(false);
    }
  };

  if (isSuccess) {
    return (
      <Container maxWidth="sm" sx={{ py: 8 }}>
        <Paper elevation={3} sx={{ p: 4 }}>
          <Box sx={{ textAlign: 'center', mb: 4 }}>
            <Email sx={{ fontSize: 60, color: 'primary.main', mb: 2 }} />
            <Typography variant="h4" component="h1" gutterBottom>
              Password Reset Successfully
            </Typography>
            <Typography variant="body1" color="text.secondary">
              Your password has been updated successfully.
            </Typography>
          </Box>

          <Alert severity="success" sx={{ mb: 3 }}>
            {message}
          </Alert>

          <Box sx={{ textAlign: 'center' }}>
            <Button
              variant="contained"
              onClick={onBackToLogin}
              size="large"
              sx={{
                backgroundColor: '#283E56',
                '&:hover': {
                  backgroundColor: '#1e2f42'
                }
              }}
            >
              Go to Login
            </Button>
          </Box>
        </Paper>
      </Container>
    );
  }

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
            Forgot Password
          </Typography>
          <Typography variant="body1" color="text.secondary">
            Enter your email address and create a new password
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
            placeholder="Enter your email address"
            disabled={isLoading}
          />

          <TextField
            fullWidth
            label="New Password"
            type="password"
            value={newPassword}
            onChange={(e) => setNewPassword(e.target.value)}
            margin="normal"
            required
            autoComplete="new-password"
            placeholder="Enter your new password"
            disabled={isLoading}
          />

          <TextField
            fullWidth
            label="Confirm New Password"
            type="password"
            value={confirmPassword}
            onChange={(e) => setConfirmPassword(e.target.value)}
            margin="normal"
            required
            autoComplete="new-password"
            placeholder="Confirm your new password"
            disabled={isLoading}
          />

          {error && (
            <Alert severity="error" sx={{ mt: 2 }}>
              {error}
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
            {isLoading ? <CircularProgress size={24} /> : 'Reset Password'}
          </Button>

          <Divider sx={{ my: 2 }} />

          <Box sx={{ textAlign: 'center' }}>
            <Link
              component="button"
              type="button"
              onClick={onBackToLogin}
              sx={{ cursor: 'pointer', display: 'flex', alignItems: 'center', justifyContent: 'center' }}
            >
              <ArrowBack sx={{ mr: 1, fontSize: 18 }} />
              Back to Login
            </Link>
          </Box>
        </form>
      </Paper>
    </Container>
  );
};

export default ForgotPassword;