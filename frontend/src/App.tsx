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
import ResultsTable from './components/ResultsTable';
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
    <Container maxWidth="lg" sx={{ py: 4 }}>
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
      
      <Box sx={{ mb: 4 }}>
        <Paper elevation={3} sx={{ p: 3 }}>
          <Typography variant="h6" gutterBottom>
            Search Information
          </Typography>
          <SearchForm onSubmit={handleSearch} />
        </Paper>
      </Box>

      {error && (
        <Alert severity="error" sx={{ mb: 3 }}>
          {error}
        </Alert>
      )}

      {results && (
        <Box>
          <Paper elevation={3} sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Search Results
            </Typography>
            <ResultsTable data={results} />
          </Paper>
        </Box>
      )}

      <Backdrop
        sx={{ color: '#fff', zIndex: (theme) => theme.zIndex.drawer + 1 }}
        open={loading}
      >
        <CircularProgress color="inherit" />
        <Typography variant="h6" sx={{ ml: 2 }}>
          Searching Experian database...
        </Typography>
      </Backdrop>
    </Container>
  );
}

export default App;