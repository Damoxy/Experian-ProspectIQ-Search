import React, { useState, useEffect } from 'react';
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
  Chip,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  IconButton,
  Button,
  TablePagination,
} from '@mui/material';
import { Person, Home, Phone, Email, Badge, AttachMoney, TrendingUp, DateRange, Schedule, ArrowBack, Search as SearchIcon } from '@mui/icons-material';
import { AuthProvider, useAuth } from './contexts/AuthContext';
import AuthPage from './components/AuthPage';
import Header from './components/Header';
import SearchForm from './components/SearchForm';
import TabbedResults from './components/TabbedResults';
import BackToTop from './components/BackToTop';
import { searchKnowledgeCore, validatePhoneNumbers, getRecentSearches, clearRecentSearches } from './services/api';
import { SearchFormData, SearchResult } from './types';

// Create enhanced modern theme with gradient background
const lightTheme = createTheme({
  palette: {
    mode: 'light',
    primary: {
      main: '#2E3B55',
      light: '#4A5D7A',
      dark: '#1C2433',
    },
    secondary: {
      main: '#00C853',
      light: '#5EFC82',
      dark: '#009624',
    },
    background: {
      default: '#E5E7EB',
      paper: 'rgba(255, 255, 255, 0.95)',
    },
    text: {
      primary: '#2E3B55',
      secondary: '#5A6C7D',
    },
  },
  components: {
    MuiCssBaseline: {
      styleOverrides: {
        body: {
          background: '#E5E7EB',
          minHeight: '100vh',
          backgroundAttachment: 'fixed',
        },
      },
    },
    MuiPaper: {
      styleOverrides: {
        root: {
          background: 'rgba(255, 255, 255, 0.95)',
          backdropFilter: 'blur(10px)',
          border: '1px solid rgba(255, 255, 255, 0.2)',
          boxShadow: '0 8px 32px rgba(0, 0, 0, 0.1)',
        },
      },
    },
    MuiContainer: {
      styleOverrides: {
        root: {
          background: 'transparent',
        },
      },
    },
  },
});

// Main app content component (protected)
const AppContent: React.FC = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [results, setResults] = useState<SearchResult | null>(null);
  const [searchCriteria, setSearchCriteria] = useState<SearchFormData | null>(null);
  const [recentSearches, setRecentSearches] = useState<any[]>([]);
  const [showRecentSearchesPage, setShowRecentSearchesPage] = useState(false);
  const [paginationPage, setPaginationPage] = useState(0);
  const [paginationRowsPerPage, setPaginationRowsPerPage] = useState(10);
  const { isAuthenticated, isLoading } = useAuth();

  // Load recent searches on mount and after successful search
  useEffect(() => {
    if (isAuthenticated && !isLoading) {
      loadRecentSearches();
    }
  }, [isAuthenticated, isLoading]);

  const loadRecentSearches = async () => {
    try {
      const response = await getRecentSearches();
      if (response && response.searches) {
        setRecentSearches(response.searches);
      }
    } catch (err) {
      console.warn('Failed to load recent searches:', err instanceof Error ? err.message : 'Unknown error');
      // Don't fail the app if recent searches fail to load
    }
  };

  const clearSearchHistory = async () => {
    if (window.confirm('Are you sure you want to clear all search history? This cannot be undone.')) {
      try {
        await clearRecentSearches();
        setRecentSearches([]);
      } catch (err) {
        console.error('Failed to clear search history:', err);
      }
    }
  };

  const handleSearch = async (formData: SearchFormData) => {
    setLoading(true);
    setError(null);
    setResults(null);
    setSearchCriteria(formData); // Store the search criteria

    try {
      const data = await searchKnowledgeCore(formData);
      
      // If the result comes from Experian fallback (no database records found),
      // also call phone validation to enrich contact information
      if (data && data.fallback_source === 'experian_api' && data.database_records_found === 0) {
        try {
          console.log('Database records not found, attempting phone validation...');
          const phoneData = await validatePhoneNumbers(formData);
          
          // Merge phone validation data with the main results
          if (phoneData && phoneData.phone_validation) {
            data.phone_validation = phoneData.phone_validation;
            console.log('Phone validation data merged successfully');
          }
        } catch (phoneErr) {
          console.warn('Phone validation failed:', phoneErr instanceof Error ? phoneErr.message : 'Unknown error');
          // Don't fail the entire search if phone validation fails
        }
      }
      
      setResults(data);
      // Reload recent searches after successful search
      loadRecentSearches();
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
      
      {showRecentSearchesPage ? (
        // Recent Searches Full Page - CRM Table Format
        <Box sx={{ width: '100%', height: '100%', display: 'flex', flexDirection: 'column', backgroundColor: '#f5f5f5' }}>
          <Box sx={{ p: 3, backgroundColor: 'white', borderBottom: '1px solid #e0e0e0' }}>
            <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                <IconButton 
                  onClick={() => setShowRecentSearchesPage(false)}
                  sx={{ color: '#2E3B55' }}
                >
                  <ArrowBack />
                </IconButton>
                <Box>
                  <Typography variant="h5" sx={{ fontWeight: 600, color: '#2E3B55' }}>
                    Recent Searches
                  </Typography>
                </Box>
              </Box>
              <Button
                variant="outlined"
                color="error"
                size="small"
                onClick={clearSearchHistory}
              >
                Clear All
              </Button>
            </Box>
          </Box>

          <Box sx={{ flex: 1, overflow: 'auto', p: 2 }}>
            <TableContainer component={Paper} sx={{ backgroundColor: 'white' }}>
              {recentSearches && recentSearches.length > 0 ? (
                <>
                  <Table sx={{ minWidth: 900 }}>
                    <TableHead>
                      <TableRow sx={{ backgroundColor: '#f5f5f5', borderBottom: '2px solid #2E3B55' }}>
                        <TableCell sx={{ fontWeight: 700, color: '#2E3B55', width: '8%', borderRight: '1px solid #e0e0e0' }}>No.</TableCell>
                        <TableCell sx={{ fontWeight: 700, color: '#2E3B55', width: '14%', borderRight: '1px solid #e0e0e0' }}>First Name</TableCell>
                        <TableCell sx={{ fontWeight: 700, color: '#2E3B55', width: '14%', borderRight: '1px solid #e0e0e0' }}>Last Name</TableCell>
                        <TableCell sx={{ fontWeight: 700, color: '#2E3B55', width: '20%', borderRight: '1px solid #e0e0e0' }}>Address</TableCell>
                        <TableCell sx={{ fontWeight: 700, color: '#2E3B55', width: '15%', borderRight: '1px solid #e0e0e0' }}>City, State, ZIP</TableCell>
                        <TableCell sx={{ fontWeight: 700, color: '#2E3B55', width: '14%', borderRight: '1px solid #e0e0e0' }}>Searched</TableCell>
                        <TableCell sx={{ fontWeight: 700, color: '#2E3B55', width: '15%', textAlign: 'center' }}>Action</TableCell>
                      </TableRow>
                    </TableHead>
                    <TableBody>
                      {recentSearches
                        .slice(paginationPage * paginationRowsPerPage, paginationPage * paginationRowsPerPage + paginationRowsPerPage)
                        .map((search, index) => (
                          <TableRow 
                            key={search.id}
                            sx={{ 
                              '&:hover': { 
                                backgroundColor: 'rgba(46, 59, 85, 0.05)',
                                transition: 'background-color 0.2s ease'
                              },
                              borderBottom: '1px solid #e0e0e0'
                            }}
                          >
                            <TableCell sx={{ color: '#2E3B55', fontWeight: 500, borderRight: '1px solid #e0e0e0' }}>
                              {paginationPage * paginationRowsPerPage + index + 1}
                            </TableCell>
                            <TableCell sx={{ color: '#2E3B55', borderRight: '1px solid #e0e0e0' }}>{search.first_name || '-'}</TableCell>
                            <TableCell sx={{ color: '#2E3B55', borderRight: '1px solid #e0e0e0' }}>{search.last_name || '-'}</TableCell>
                            <TableCell sx={{ color: '#5A6C7D', borderRight: '1px solid #e0e0e0' }}>{search.street || '-'}</TableCell>
                            <TableCell sx={{ color: '#5A6C7D', borderRight: '1px solid #e0e0e0' }}>
                              {[search.city, search.state, search.zip_code].filter(Boolean).join(', ') || '-'}
                            </TableCell>
                            <TableCell sx={{ color: '#999', fontSize: '0.9rem', borderRight: '1px solid #e0e0e0' }}>{search.date}</TableCell>
                            <TableCell sx={{ textAlign: 'center' }}>
                              <IconButton
                                size="small"
                                onClick={() => {
                                  const formData: SearchFormData = {
                                    FIRST_NAME: search.first_name || '',
                                    LAST_NAME: search.last_name || '',
                                    STREET1: search.street || '',
                                    STREET2: '',
                                    CITY: search.city || '',
                                    STATE: search.state || '',
                                    ZIP: search.zip_code || '',
                                  };
                                  setShowRecentSearchesPage(false);
                                  handleSearch(formData);
                                }}
                                sx={{ color: '#2E3B55', '&:hover': { backgroundColor: 'rgba(46, 59, 85, 0.1)' } }}
                              >
                                <SearchIcon />
                              </IconButton>
                            </TableCell>
                          </TableRow>
                        ))}
                    </TableBody>
                  </Table>
                  <TablePagination
                    rowsPerPageOptions={[10, 25, 50]}
                    component="div"
                    count={recentSearches.length}
                    rowsPerPage={paginationRowsPerPage}
                    page={paginationPage}
                    onPageChange={(event, newPage) => setPaginationPage(newPage)}
                    onRowsPerPageChange={(event) => {
                      setPaginationRowsPerPage(parseInt(event.target.value, 10));
                      setPaginationPage(0);
                    }}
                    sx={{
                      backgroundColor: '#f9f9f9',
                      borderTop: '1px solid #e0e0e0',
                      '& .MuiTablePagination-select': {
                        marginRight: '8px',
                      }
                    }}
                  />
                </>
              ) : (
                <Box sx={{ p: 6, textAlign: 'center' }}>
                  <Typography variant="body2" sx={{ color: '#999' }}>
                    No recent searches yet
                  </Typography>
                </Box>
              )}
            </TableContainer>
          </Box>
        </Box>
      ) : (
        // Results layout (grid with left search, right results) - ALWAYS SHOWN
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
              
              {/* Recent Searches Section */}
              <Box sx={{ mt: 3, pt: 3, borderTop: '1px solid rgba(0,0,0,0.1)' }}>
                <Typography variant="h6" sx={{ mb: 2, fontWeight: 600, fontSize: '1rem' }}>
                  Recent Searches
                </Typography>
                <Box sx={{ display: 'flex', flexDirection: 'column', gap: 1 }}>
                  {recentSearches && recentSearches.length > 0 ? (
                    recentSearches.slice(0, 5).map((search) => (
                      <Box 
                        key={search.id}
                        sx={{ 
                          p: 1.5, 
                          borderRadius: 1.5, 
                          backgroundColor: 'rgba(52, 152, 219, 0.04)',
                          border: '1px solid rgba(52, 152, 219, 0.08)',
                          cursor: 'pointer',
                          transition: 'all 0.2s ease',
                          '&:hover': {
                            backgroundColor: 'rgba(52, 152, 219, 0.08)',
                            borderColor: 'rgba(52, 152, 219, 0.15)',
                            transform: 'translateY(-1px)'
                          }
                        }}
                        onClick={() => {
                          const formData: SearchFormData = {
                            FIRST_NAME: search.first_name || '',
                            LAST_NAME: search.last_name || '',
                            STREET1: search.street || '',
                            STREET2: '',
                            CITY: search.city || '',
                            STATE: search.state || '',
                            ZIP: search.zip_code || '',
                          };
                          handleSearch(formData);
                        }}
                      >
                        <Typography variant="body2" sx={{ fontWeight: 600, color: '#2C3E50', fontSize: '0.85rem', mb: 0.3 }}>
                          {search.name}
                        </Typography>
                        <Typography variant="caption" sx={{ color: '#566573', fontSize: '0.75rem', display: 'block', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap', mb: 0.3 }}>
                          {search.address}
                        </Typography>
                        <Typography variant="caption" sx={{ color: '#7B8794', fontSize: '0.7rem' }}>
                          {search.date}
                        </Typography>
                      </Box>
                    ))
                  ) : (
                    <Typography variant="caption" sx={{ color: '#999', fontStyle: 'italic' }}>
                      No recent searches
                    </Typography>
                  )}
                </Box>
                {recentSearches && recentSearches.length > 0 && (
                  <Typography 
                    variant="caption" 
                    sx={{ 
                      color: '#3498db', 
                      cursor: 'pointer', 
                      mt: 1.5, 
                      display: 'block',
                      fontWeight: 600,
                      textAlign: 'center',
                      '&:hover': { textDecoration: 'underline' }
                    }}
                    onClick={() => setShowRecentSearchesPage(true)}
                  >
                    View all ({recentSearches.length})
                  </Typography>
                )}
              </Box>
              
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
                  background: 'linear-gradient(to bottom, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0.05) 30%, transparent 60%)',
                  backdropFilter: 'blur(10px)',
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
                    top: '-3px',
                    left: '-3px',
                    right: '-3px',
                    bottom: '-3px',
                    background: 'linear-gradient(0deg, #3498db, #2ecc71, #f39c12, #e74c3c, #9b59b6, #3498db)',
                    borderRadius: '15px',
                    zIndex: -1,
                    animation: 'rotatingBorder 4s linear infinite',
                  },
                  '&::after': {
                    content: '""',
                    position: 'absolute',
                    top: '0px',
                    left: '0px',
                    right: '0px',
                    bottom: '0px',
                    background: '#283E56',
                    borderRadius: '12px',
                    zIndex: -1,
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
                  '@keyframes rotatingBorder': {
                    '0%': {
                      background: 'linear-gradient(0deg, #3498db, #2ecc71, #f39c12, #e74c3c, #9b59b6, #3498db)',
                    },
                    '25%': {
                      background: 'linear-gradient(90deg, #3498db, #2ecc71, #f39c12, #e74c3c, #9b59b6, #3498db)',
                    },
                    '50%': {
                      background: 'linear-gradient(180deg, #3498db, #2ecc71, #f39c12, #e74c3c, #9b59b6, #3498db)',
                    },
                    '75%': {
                      background: 'linear-gradient(270deg, #3498db, #2ecc71, #f39c12, #e74c3c, #9b59b6, #3498db)',
                    },
                    '100%': {
                      background: 'linear-gradient(360deg, #3498db, #2ecc71, #f39c12, #e74c3c, #9b59b6, #3498db)',
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
                <Box sx={{ display: 'grid', gridTemplateColumns: '1fr 1.5fr', gap: '32px', alignItems: 'start' }}>
                  {/* LEFT COLUMN - Contact Information */}
                  <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
                    {/* Name */}
                    <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                      <Person sx={{ fontSize: 18, opacity: 0.8, flexShrink: 0 }} />
                      <Box sx={{ display: 'flex', flexDirection: 'column', gap: 0.5 }}>
                        <Typography variant="body2" sx={{ fontWeight: 600, opacity: 0.9 }}>
                          Name
                        </Typography>
                        <Typography variant="h6" sx={{ fontWeight: 600, letterSpacing: '0.3px' }}>
                          {searchCriteria.FIRST_NAME} {searchCriteria.LAST_NAME}
                        </Typography>
                      </Box>
                    </Box>

                    {/* Address */}
                    <Box sx={{ display: 'flex', alignItems: 'flex-start', gap: 1 }}>
                      <Home sx={{ fontSize: 18, opacity: 0.8, mt: 0.5, flexShrink: 0 }} />
                      <Box sx={{ display: 'flex', flexDirection: 'column', gap: 0.5 }}>
                        <Typography variant="body2" sx={{ fontWeight: 600, opacity: 0.9 }}>
                          Address
                        </Typography>
                        <Typography variant="body1" sx={{ fontWeight: 500, lineHeight: 1.4, opacity: 0.95 }}>
                          {searchCriteria.STREET1}
                          {searchCriteria.STREET2 && `, ${searchCriteria.STREET2}`}
                          <br />
                          {searchCriteria.CITY}, {searchCriteria.STATE} {searchCriteria.ZIP}
                        </Typography>
                      </Box>
                    </Box>

                    {/* Phone */}
                    {results?.source === 'database' && results?.results?.consumer_behavior?.records?.[0]?.contact_info ? (
                      <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                        <Phone sx={{ fontSize: 18, opacity: 0.8, flexShrink: 0 }} />
                        <Box sx={{ display: 'flex', flexDirection: 'column', gap: 0.5 }}>
                          <Typography variant="body2" sx={{ fontWeight: 600, opacity: 0.9 }}>
                            Phone
                          </Typography>
                          <Typography variant="body1" sx={{ fontWeight: 500, opacity: 0.95 }}>
                            {results.results.consumer_behavior.records[0].contact_info.phone || 'Not Available'}
                          </Typography>
                        </Box>
                      </Box>
                    ) : null}

                    {/* Email */}
                    {results?.source === 'database' && results?.results?.consumer_behavior?.records?.[0]?.contact_info ? (
                      <Box sx={{ display: 'flex', alignItems: 'flex-start', gap: 1 }}>
                        <Email sx={{ fontSize: 18, opacity: 0.8, mt: 0.5, flexShrink: 0 }} />
                        <Box sx={{ display: 'flex', flexDirection: 'column', gap: 0.5 }}>
                          <Typography variant="body2" sx={{ fontWeight: 600, opacity: 0.9 }}>
                            Email
                          </Typography>
                          <Typography variant="body1" sx={{ fontWeight: 500, opacity: 0.95, lineHeight: 1.4, wordBreak: 'break-word' }}>
                            {results.results.consumer_behavior.records[0].contact_info.email || 'Not Available'}
                          </Typography>
                        </Box>
                      </Box>
                    ) : null}
                  </Box>

                  {/* RIGHT COLUMN - Financial & Transaction Data */}
                  <Box sx={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: '32px', alignItems: 'start' }}>
                    {/* Giving History Column */}
                    <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
                      {/* Largest Gift */}
                      {results?.source === 'database' && results?.results?.consumer_behavior?.records?.[0]?.contact_info ? (
                        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1.5 }}>
                          <TrendingUp sx={{ fontSize: 20, opacity: 0.8, flexShrink: 0 }} />
                          <Box sx={{ display: 'flex', flexDirection: 'column', gap: 0.5 }}>
                            <Typography variant="body2" sx={{ fontWeight: 600, opacity: 0.9, fontSize: '0.85rem' }}>
                              Largest Gift
                            </Typography>
                            {(() => {
                              const value = results.results.consumer_behavior.records[0].contact_info.largest_gift;
                              if (!value || value === 'Not Available') {
                                return <Typography variant="h6" sx={{ fontWeight: 600 }}>Not Available</Typography>;
                              }
                              const parts = value.split(' (');
                              const amount = parts[0];
                              const date = parts[1] ? parts[1].replace(')', '') : null;
                              return (
                                <>
                                  <Typography variant="h6" sx={{ fontWeight: 700, color: 'white', letterSpacing: '0.3px' }}>
                                    {amount}
                                  </Typography>
                                  {date && (
                                    <Typography variant="caption" sx={{ color: 'white', fontSize: '0.75rem', opacity: 0.8 }}>
                                      {date}
                                    </Typography>
                                  )}
                                </>
                              );
                            })()}
                          </Box>
                        </Box>
                      ) : null}

                      {/* Latest Gift */}
                      {results?.source === 'database' && results?.results?.consumer_behavior?.records?.[0]?.contact_info ? (
                        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1.5 }}>
                          <Schedule sx={{ fontSize: 20, opacity: 0.8, flexShrink: 0 }} />
                          <Box sx={{ display: 'flex', flexDirection: 'column', gap: 0.5 }}>
                            <Typography variant="body2" sx={{ fontWeight: 600, opacity: 0.9, fontSize: '0.85rem' }}>
                              Latest Gift
                            </Typography>
                            {(() => {
                              const value = results.results.consumer_behavior.records[0].contact_info.latest_gift;
                              if (!value || value === 'Not Available') {
                                return <Typography variant="h6" sx={{ fontWeight: 600 }}>Not Available</Typography>;
                              }
                              const parts = value.split(' (');
                              const amount = parts[0];
                              const date = parts[1] ? parts[1].replace(')', '') : null;
                              return (
                                <>
                                  <Typography variant="h6" sx={{ fontWeight: 700, color: 'white', letterSpacing: '0.3px' }}>
                                    {amount}
                                  </Typography>
                                  {date && (
                                    <Typography variant="caption" sx={{ color: 'white', fontSize: '0.75rem', opacity: 0.8 }}>
                                      {date}
                                    </Typography>
                                  )}
                                </>
                              );
                            })()}
                          </Box>
                        </Box>
                      ) : null}

                      {/* First Gift */}
                      {results?.source === 'database' && results?.results?.consumer_behavior?.records?.[0]?.contact_info ? (
                        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1.5 }}>
                          <DateRange sx={{ fontSize: 20, opacity: 0.8, flexShrink: 0 }} />
                          <Box sx={{ display: 'flex', flexDirection: 'column', gap: 0.5 }}>
                            <Typography variant="body2" sx={{ fontWeight: 600, opacity: 0.9, fontSize: '0.85rem' }}>
                              First Gift
                            </Typography>
                            {(() => {
                              const value = results.results.consumer_behavior.records[0].contact_info.first_gift;
                              if (!value || value === 'Not Available') {
                                return <Typography variant="h6" sx={{ fontWeight: 600 }}>Not Available</Typography>;
                              }
                              const parts = value.split(' (');
                              const amount = parts[0];
                              const date = parts[1] ? parts[1].replace(')', '') : null;
                              return (
                                <>
                                  <Typography variant="h6" sx={{ fontWeight: 700, color: 'white', letterSpacing: '0.3px' }}>
                                    {amount}
                                  </Typography>
                                  {date && (
                                    <Typography variant="caption" sx={{ color: 'white', fontSize: '0.75rem', opacity: 0.8 }}>
                                      {date}
                                    </Typography>
                                  )}
                                </>
                              );
                            })()}
                          </Box>
                        </Box>
                      ) : null}
                    </Box>

                    {/* Lifetime Giving Column */}
                    <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
                      {results?.source === 'database' && results?.results?.consumer_behavior?.records?.[0]?.contact_info ? (
                        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                          <AttachMoney sx={{ fontSize: 18, opacity: 0.8, flexShrink: 0 }} />
                          <Box sx={{ display: 'flex', flexDirection: 'column', gap: 0.5 }}>
                            <Typography variant="body2" sx={{ fontWeight: 600, opacity: 0.9 }}>
                              Lifetime Giving
                            </Typography>
                            <Typography variant="body1" sx={{ fontWeight: 700, opacity: 0.95, color: 'white' }}>
                              {(() => {
                                const value = results.results.consumer_behavior.records[0].contact_info.lifetime_giving;
                                if (!value || value === 'Not Available') return 'Not Available';
                                const match = value.match(/^\$[\d,.]+(\.[ 0-9]{2})?/);
                                return match ? match[0] : value;
                              })()}
                            </Typography>
                          </Box>
                        </Box>
                      ) : null}
                    </Box>

                    {/* Constituent ID Column */}
                    <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
                      {results?.source === 'database' && results?.results?.consumer_behavior?.records?.[0]?.contact_info ? (
                        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                          <Badge sx={{ fontSize: 18, opacity: 0.8, flexShrink: 0 }} />
                          <Box sx={{ display: 'flex', flexDirection: 'column', gap: 0.5 }}>
                            <Typography variant="body2" sx={{ fontWeight: 600, opacity: 0.9 }}>
                              Constituent ID
                            </Typography>
                            <Typography variant="body1" sx={{ fontWeight: 500, opacity: 0.95 }}>
                              {results.results.consumer_behavior.records[0].contact_info.constituent_id || 'Not Available'}
                            </Typography>
                          </Box>
                        </Box>
                      ) : null}
                    </Box>

                </Box>
                </Box>
                
                {/* Source Badge - positioned absolutely at extreme right */}
                {results?.source === 'database' || results?.message?.includes('KnowledgeCore') ? (
                  <Chip
                    label="KC/GT Database"
                    size="small"
                    sx={{
                      position: 'absolute',
                      top: 16,
                      right: 16,
                      backgroundColor: '#4caf50', // Green for database
                      color: 'white',
                      fontWeight: 600,
                      fontSize: '0.75rem',
                      height: 24,
                      boxShadow: '0 2px 4px rgba(0,0,0,0.2)',
                      border: '1px solid rgba(255,255,255,0.3)',
                      animation: 'fadeInRight 0.8s ease-out 0.6s both',
                      '&:hover': {
                        transform: 'translateY(-1px)',
                        boxShadow: '0 4px 8px rgba(0,0,0,0.3)',
                      },
                      transition: 'all 0.3s ease',
                    }}
                  />
                ) : (
                  <Box
                    component="img"
                    src="/Experian-Logo.png"
                    alt="Experian Logo"
                    sx={{
                      position: 'absolute',
                      top: 16,
                      right: 16,
                      height: 40,
                      width: 'auto',
                      maxWidth: 150,
                      animation: 'fadeInRight 0.8s ease-out 0.6s both',
                      '&:hover': {
                        filter: 'drop-shadow(0 4px 8px rgba(0,0,0,0.2))',
                        transform: 'scale(1.02)',
                      },
                      transition: 'all 0.3s ease',
                    }}
                  />
                )}
              </Box>
            )}

            
            <Paper elevation={3} sx={{ 
              p: 3, 
              minHeight: 'calc(100vh - 140px)', 
              position: 'relative', 
              zIndex: 10,
              marginTop: 0,
              borderRadius: 3
            }}>
              <Typography variant="h6" gutterBottom>
                Search Results
              </Typography>
              {results ? (
                <TabbedResults data={results} searchCriteria={searchCriteria || undefined} />
              ) : (
                <Box sx={{ py: 4, textAlign: 'center', color: '#999' }}>
                  <Typography variant="body1">
                    No search results yet. Enter a name and click Search to get started.
                  </Typography>
                </Box>
              )}
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