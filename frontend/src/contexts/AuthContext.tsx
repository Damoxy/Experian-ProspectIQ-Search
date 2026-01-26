import React, { createContext, useContext, useState, useEffect, ReactNode, useRef } from 'react';
import { User, AuthResponse, LoginRequest, SignupRequest } from '../types';
import { authAPI } from '../services/api';

interface AuthContextType {
  user: User | null;
  token: string | null;
  login: (credentials: LoginRequest) => Promise<void>;
  signup: (userData: SignupRequest) => Promise<void>;
  logout: () => void;
  isLoading: boolean;
  isAuthenticated: boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

interface AuthProviderProps {
  children: ReactNode;
}

// Inactivity timeout in milliseconds (10 minutes)
const INACTIVITY_TIMEOUT = 10 * 60 * 1000;

export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [token, setToken] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const inactivityTimerRef = useRef<NodeJS.Timeout | null>(null);

  // Initialize auth state from localStorage
  useEffect(() => {
    const savedToken = localStorage.getItem('authToken');
    const savedUser = localStorage.getItem('authUser');
    
    if (savedToken && savedUser) {
      setToken(savedToken);
      setUser(JSON.parse(savedUser));
    }
    setIsLoading(false);
  }, []);

  // Setup inactivity timeout
  useEffect(() => {
    if (!token) {
      // Clear timeout if user is not authenticated
      if (inactivityTimerRef.current) {
        clearTimeout(inactivityTimerRef.current);
      }
      return;
    }

    // Function to reset the inactivity timer
    const resetInactivityTimer = () => {
      // Clear existing timer
      if (inactivityTimerRef.current) {
        clearTimeout(inactivityTimerRef.current);
      }

      // Set new timer - logout after inactivity
      inactivityTimerRef.current = setTimeout(() => {
        console.log('User inactive for 10 minutes, logging out...');
        logout();
        // Redirect to home page
        window.location.href = '/';
      }, INACTIVITY_TIMEOUT);
    };

    // Reset timer on user activity
    const handleUserActivity = () => {
      resetInactivityTimer();
    };

    // Add event listeners for user activity
    const events = ['mousedown', 'keydown', 'scroll', 'touchstart', 'click'];
    events.forEach(event => {
      window.addEventListener(event, handleUserActivity);
    });

    // Initialize the timer
    resetInactivityTimer();

    // Cleanup
    return () => {
      events.forEach(event => {
        window.removeEventListener(event, handleUserActivity);
      });
      if (inactivityTimerRef.current) {
        clearTimeout(inactivityTimerRef.current);
      }
    };
  }, [token]);

  const login = async (credentials: LoginRequest) => {
    setIsLoading(true);
    try {
      const response: AuthResponse = await authAPI.login(credentials);
      
      setToken(response.access_token);
      setUser(response.user);
      
      // Save to localStorage
      localStorage.setItem('authToken', response.access_token);
      localStorage.setItem('authUser', JSON.stringify(response.user));
      
    } catch (error) {
      throw error;
    } finally {
      setIsLoading(false);
    }
  };

  const signup = async (userData: SignupRequest) => {
    setIsLoading(true);
    try {
      const response: AuthResponse = await authAPI.signup(userData);
      
      setToken(response.access_token);
      setUser(response.user);
      
      // Save to localStorage
      localStorage.setItem('authToken', response.access_token);
      localStorage.setItem('authUser', JSON.stringify(response.user));
      
    } catch (error) {
      throw error;
    } finally {
      setIsLoading(false);
    }
  };

  const logout = () => {
    setToken(null);
    setUser(null);
    localStorage.removeItem('authToken');
    localStorage.removeItem('authUser');
    
    // Clear inactivity timer
    if (inactivityTimerRef.current) {
      clearTimeout(inactivityTimerRef.current);
    }
  };

  const value: AuthContextType = {
    user,
    token,
    login,
    signup,
    logout,
    isLoading,
    isAuthenticated: !!user && !!token,
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = (): AuthContextType => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};