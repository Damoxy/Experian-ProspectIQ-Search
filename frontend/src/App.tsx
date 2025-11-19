import React, { useState } from 'react';
import {
  Container,
  Typography,
  Paper,
  Box,
  Alert,
  CircularProgress,
  Backdrop,
} from '@mui/material';
import SearchForm from './components/SearchForm';
import TabbedResults from './components/TabbedResults';
import BackToTop from './components/BackToTop';
import { searchExperian } from './services/api';
import { SearchFormData, SearchResult } from './types';

function App() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [results, setResults] = useState<SearchResult | null>(null);

  const handleSearch = async (formData: SearchFormData) => {
    setLoading(true);
    setError(null);
    setResults(null);

    try {
      const data = await searchExperian(formData);
      setResults(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An unexpected error occurred');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Container maxWidth={false} sx={{ py: 4, px: 3, maxWidth: '100vw' }}>
      <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'flex-start', mb: 4 }}>
        <img 
          src="/knowledgecore.jpeg" 
          alt="Knowledge Core Logo" 
          style={{ height: '60px', marginRight: '20px' }}
        />
        <Typography variant="h4" component="h1" sx={{ color: 'white' }}>
          Experian Prospect IQ Search
        </Typography>
      </Box>
      
      <Box sx={{ 
        display: 'grid', 
        gridTemplateColumns: results ? '400px 1fr' : '1fr',
        gap: 3,
        minHeight: 'calc(100vh - 200px)',
        transition: 'grid-template-columns 0.3s ease-in-out'
      }}>
        {/* Search Panel */}
        <Box sx={{ 
          position: results ? 'sticky' : 'relative',
          top: results ? 20 : 0,
          height: results ? 'fit-content' : 'auto'
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
        {results && (
          <Box sx={{ minWidth: 0, overflow: 'hidden' }}>
            <Paper elevation={3} sx={{ p: 3, height: 'fit-content' }}>
              <Typography variant="h6" gutterBottom>
                Search Results
              </Typography>
              <TabbedResults data={results} />
            </Paper>
          </Box>
        )}
      </Box>

      <Backdrop
        sx={{ color: '#fff', zIndex: (theme) => theme.zIndex.drawer + 1 }}
        open={loading}
      >
        <CircularProgress color="inherit" />
        <Typography variant="h6" sx={{ ml: 2 }}>
          Searching Experian database...
        </Typography>
      </Backdrop>
      
      <BackToTop />
    </Container>
  );
}

export default App;