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
import { Person, Home } from '@mui/icons-material';
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
  const [searchCriteria, setSearchCriteria] = useState<SearchFormData | null>(null);
  const { isAuthenticated, isLoading } = useAuth();

  const handleSearch = async (formData: SearchFormData) => {
    setLoading(true);
    setError(null);
    setResults(null);
    setSearchCriteria(formData); // Store the search criteria

    try {
      const data = await searchKnowledgeCore(formData);
      setResults(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An unexpected error occurred');
      setSearchCriteria(null); // Clear criteria on error
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
      <Container maxWidth={false} sx={{ pt: 12, pb: 4, px: 3, maxWidth: '100vw', position: 'relative' }}>
      
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
            top: 80, // Account for sticky header height (64px + margin)
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
          <Box sx={{ minWidth: 0, overflow: 'visible', height: 'fit-content', position: 'relative' }}>
            {/* Fade mask to hide content behind sticky header */}
            {searchCriteria && (
              <Box
                sx={{
                  position: 'fixed',
                  top: 64, // Start right after main header
                  left: 440, // Start after search panel (400px + 40px gap)
                  right: 24, // Match container padding
                  height: 140, // Cover area where sticky header will be
                  background: 'linear-gradient(to bottom, rgba(255,255,255,0.95) 0%, rgba(255,255,255,0.9) 30%, rgba(255,255,255,0.7) 60%, transparent 100%)',
                  zIndex: 1150,
                  pointerEvents: 'none',
                }}
              />
            )}
            
            {/* Search Summary Header - Sticky within results column */}
            {searchCriteria && (
              <Box
                sx={{ 
                  p: 2.5, 
                  mb: 3, 
                  backgroundColor: '#283E56',
                  color: 'white',
                  borderRadius: 3,
                  position: 'sticky',
                  top: 80, // Account for sticky header height (64px + margin)
                  zIndex: 1200,
                  overflow: 'visible',
                  boxShadow: '0 4px 12px rgba(0, 0, 0, 0.3), 0 2px 8px rgba(0, 0, 0, 0.15)',
                  '&::before': {
                    content: '""',
                    position: 'absolute',
                    top: 0,
                    left: 0,
                    right: 0,
                    height: '4px',
                    background: 'linear-gradient(90deg, #3498db, #2ecc71, #f39c12, #e74c3c)',
                    borderRadius: '12px 12px 0 0',
                  },
                  animation: 'slideInDown 0.6s ease-out',
                  '@keyframes slideInDown': {
                    '0%': {
                      transform: 'translateY(-30px)',
                      opacity: 0,
                    },
                    '100%': {
                      transform: 'translateY(0)',
                      opacity: 1,
                    },
                  },
                  '&:hover': {
                    transform: 'translateY(-2px)',
                    boxShadow: '0 8px 25px rgba(40, 62, 86, 0.3)',
                    transition: 'all 0.3s ease',
                  },
                  transition: 'all 0.3s ease',
                }}
              >
                <Box sx={{ display: 'grid', gridTemplateColumns: 'auto 1fr', gap: 2, alignItems: 'start' }}>
                  {/* Name Row */}
                  <Box 
                    sx={{ 
                      display: 'flex', 
                      alignItems: 'center', 
                      minWidth: 100,
                      animation: 'fadeInLeft 0.8s ease-out 0.2s both',
                      '@keyframes fadeInLeft': {
                        '0%': {
                          transform: 'translateX(-20px)',
                          opacity: 0,
                        },
                        '100%': {
                          transform: 'translateX(0)',
                          opacity: 1,
                        },
                      },
                    }}
                  >
                    <Person sx={{ 
                      mr: 1, 
                      fontSize: 18, 
                      opacity: 0.8,
                      animation: 'pulse 2s infinite',
                      '@keyframes pulse': {
                        '0%, 100%': { opacity: 0.8 },
                        '50%': { opacity: 1 },
                      },
                    }} />
                    <Typography variant="body2" sx={{ fontWeight: 600, opacity: 0.9 }}>
                      Name:
                    </Typography>
                  </Box>
                  <Typography 
                    variant="h6" 
                    sx={{ 
                      fontWeight: 600, 
                      letterSpacing: '0.3px',
                      textShadow: '0 1px 2px rgba(0,0,0,0.2)',
                      animation: 'fadeInRight 0.8s ease-out 0.3s both',
                      '@keyframes fadeInRight': {
                        '0%': {
                          transform: 'translateX(20px)',
                          opacity: 0,
                        },
                        '100%': {
                          transform: 'translateX(0)',
                          opacity: 1,
                        },
                      },
                    }}
                  >
                    {searchCriteria.FIRST_NAME} {searchCriteria.LAST_NAME}
                  </Typography>
                  
                  {/* Address Row */}
                  <Box 
                    sx={{ 
                      display: 'flex', 
                      alignItems: 'center', 
                      minWidth: 100,
                      animation: 'fadeInLeft 0.8s ease-out 0.4s both',
                    }}
                  >
                    <Home sx={{ 
                      mr: 1, 
                      fontSize: 18, 
                      opacity: 0.8,
                      animation: 'pulse 2s infinite 0.5s',
                    }} />
                    <Typography variant="body2" sx={{ fontWeight: 600, opacity: 0.9 }}>
                      Address:
                    </Typography>
                  </Box>
                  <Typography 
                    variant="body1" 
                    sx={{ 
                      fontWeight: 500, 
                      lineHeight: 1.4,
                      opacity: 0.95,
                      animation: 'fadeInRight 0.8s ease-out 0.5s both',
                    }}
                  >
                    {searchCriteria.STREET1}
                    {searchCriteria.STREET2 && `, ${searchCriteria.STREET2}`}
                    <br />
                    {searchCriteria.CITY}, {searchCriteria.STATE} {searchCriteria.ZIP}
                  </Typography>
                </Box>
              </Box>
            )}
            
            <Paper elevation={3} sx={{ 
              p: 3, 
              height: 'fit-content', 
              position: 'relative', 
              zIndex: 10,
              backgroundColor: '#ffffff',
              marginTop: 0
            }}>
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