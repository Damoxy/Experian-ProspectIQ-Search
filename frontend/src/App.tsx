import React, { useState } from 'react';
import {
  Container,
  Typography,
  Paper,
  Box,
  Alert,
  CircularProgress,
  Backdrop,
  CssBaseline,
  ThemeProvider,
  createTheme,
} from '@mui/material';
import { AuthProvider, useAuth } from './contexts/AuthContext';
import AuthPage from './components/AuthPage';
import Header from './components/Header';
import SearchForm from './components/SearchForm';
import TabbedResults from './components/TabbedResults';
import BackToTop from './components/BackToTop';
import AnimatedBubbles from './components/AnimatedBubbles';
import { searchKnowledgeCore } from './services/api';
import { SearchFormData, SearchResult } from './types';

// Create light theme (original white background)
const lightTheme = createTheme({
  palette: {
    mode: 'light',
    primary: {
      main: '#1976d2',
    },
    background: {
      default: '#ffffff',
      paper: '#ffffff',
    },
  },
});

// Main app content component (protected)
const AppContent: React.FC = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [results, setResults] = useState<SearchResult | null>(null);
  const { isAuthenticated, isLoading } = useAuth();

  const handleSearch = async (formData: SearchFormData) => {
    setLoading(true);
    setError(null);
    setResults(null);

    try {
      const data = await searchKnowledgeCore(formData);
      setResults(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An unexpected error occurred');
    } finally {
      setLoading(false);
    }
  };

  // Show loading spinner while checking authentication
  if (isLoading) {
    return (
      <Box sx={{ 
        display: 'flex', 
        justifyContent: 'center', 
        alignItems: 'center', 
        minHeight: '100vh' 
      }}>
        <CircularProgress size={60} />
      </Box>
    );
  }

  // Show auth page if not authenticated
  if (!isAuthenticated) {
    return <AuthPage />;
  }

  // Authenticated user dashboard
  return (
    <>
      <Header />
      <Container maxWidth={false} sx={{ py: 4, px: 3, maxWidth: '100vw', position: 'relative' }}>
      
      {!results ? (
        // Centered search layout with bubbles
        <Box sx={{ 
          position: 'relative',
          minHeight: 'calc(100vh - 200px)',
          display: 'flex',
          justifyContent: 'center',
          alignItems: 'flex-start',
          pt: 4
        }}>
          {/* Background bubbles */}
          <Box sx={{ 
            position: 'absolute', 
            top: 0,
            left: 0,
            width: '100%',
            height: '100%',
            overflow: 'hidden',
            borderRadius: 2,
            background: 'linear-gradient(135deg, #ffffff 0%, #e3f2fd 50%, #bbdefb 100%)',
            zIndex: 0
          }}>
            <AnimatedBubbles />
          </Box>
          
          {/* Centered Search Panel */}
          <Box sx={{ 
            position: 'relative',
            zIndex: 1,
            width: '100%',
            maxWidth: '500px'
          }}>
            <Paper elevation={6} sx={{ p: 4, borderRadius: 3 }}>
              <Typography variant="h5" gutterBottom sx={{ textAlign: 'center', color: '#283E56', fontWeight: 600, mb: 3 }}>
                Search Information
              </Typography>
              <SearchForm onSubmit={handleSearch} />
              
              {error && (
                <Alert severity="error" sx={{ mt: 3 }}>
                  {error}
                </Alert>
              )}
            </Paper>
          </Box>
        </Box>
      ) : (
        // Results layout (grid with left search, right results)
        <Box sx={{ 
          display: 'grid', 
          gridTemplateColumns: '400px 1fr',
          gap: 3,
          minHeight: 'calc(100vh - 200px)',
        }}>
          {/* Search Panel */}
          <Box sx={{ 
            position: 'sticky',
            top: 20,
            height: 'fit-content'
          }}>
            <Paper elevation={3} sx={{ p: 3, height: 'fit-content' }}>
              <Typography variant="h6" gutterBottom>
                Search Information
              </Typography>
              <SearchForm onSubmit={handleSearch} />
              
              {error && (
                <Alert severity="error" sx={{ mt: 3 }}>
                  {error}
                </Alert>
              )}
            </Paper>
          </Box>

          {/* Results Panel */}
          <Box sx={{ minWidth: 0, overflow: 'hidden' }}>
            <Paper elevation={3} sx={{ p: 3, height: 'fit-content' }}>
              <Typography variant="h6" gutterBottom>
                Search Results
              </Typography>
              <TabbedResults data={results} />
            </Paper>
          </Box>
        </Box>
      )}

      <Backdrop
        sx={{ color: '#fff', zIndex: (theme) => theme.zIndex.drawer + 1 }}
        open={loading}
      >
        <CircularProgress color="inherit" />
        <Typography variant="h6" sx={{ ml: 2 }}>
          Searching Knowledge Core database...
        </Typography>
      </Backdrop>
      
      <BackToTop />
      </Container>
    </>
  );
};

// Main App component with providers
function App() {
  return (
    <ThemeProvider theme={lightTheme}>
      <CssBaseline />
      <AuthProvider>
        <AppContent />
      </AuthProvider>
    </ThemeProvider>
  );
}

export default App;