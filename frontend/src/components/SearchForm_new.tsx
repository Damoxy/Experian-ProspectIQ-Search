import React, { useState } from 'react';
import {
  Grid,
  TextField,
  Button,
  Box,
  InputAdornment,
  Typography,
  IconButton,
  Card,
  CardContent,
} from '@mui/material';
import {
  Person,
  Home,
  LocationCity,
  Public,
  MailOutline,
  Add,
  Delete,
  Search,
  Clear,
} from '@mui/icons-material';
import { SearchFormData } from '../types';

interface SearchFormProps {
  onSubmit: (data: SearchFormData[]) => void;
}

const emptyFormData: SearchFormData = {
  FIRST_NAME: '',
  LAST_NAME: '',
  STREET1: '',
  STREET2: '',
  CITY: '',
  STATE: '',
  ZIP: '',
};

const SearchForm: React.FC<SearchFormProps> = ({ onSubmit }) => {
  const [prospects, setProspects] = useState<SearchFormData[]>([{ ...emptyFormData }]);

  const handleInputChange = (index: number, field: keyof SearchFormData) => (
    event: React.ChangeEvent<HTMLInputElement>
  ) => {
    setProspects(prev => prev.map((prospect, i) => 
      i === index ? { ...prospect, [field]: event.target.value } : prospect
    ));
  };

  const addProspect = () => {
    setProspects(prev => [...prev, { ...emptyFormData }]);
  };

  const removeProspect = (index: number) => {
    if (prospects.length > 1) {
      setProspects(prev => prev.filter((_, i) => i !== index));
    }
  };

  const handleSubmit = (event: React.FormEvent) => {
    event.preventDefault();
    
    // Filter out empty prospects (those without at least first name and last name)
    const validProspects = prospects.filter(prospect => 
      prospect.FIRST_NAME.trim() && prospect.LAST_NAME.trim()
    );
    
    if (validProspects.length > 0) {
      onSubmit(validProspects);
    }
  };

  const resetForm = () => {
    setProspects([{ ...emptyFormData }]);
  };

  return (
    <Box component="form" onSubmit={handleSubmit}>
      {prospects.map((prospect, index) => (
        <Card key={index} elevation={2} sx={{ mb: 3, borderRadius: 2 }}>
          <CardContent>
            <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
              <Typography variant="h6" sx={{ color: '#1565c0', fontWeight: 500 }}>
                Prospect #{index + 1}
              </Typography>
              {prospects.length > 1 && (
                <IconButton
                  onClick={() => removeProspect(index)}
                  color="error"
                  size="small"
                >
                  <Delete />
                </IconButton>
              )}
            </Box>
            
            <Grid container spacing={3}>
              <Grid item xs={12} sm={6}>
                <TextField
                  fullWidth
                  label="First Name"
                  value={prospect.FIRST_NAME}
                  onChange={handleInputChange(index, 'FIRST_NAME')}
                  InputProps={{
                    startAdornment: (
                      <InputAdornment position="start">
                        <Person />
                      </InputAdornment>
                    ),
                  }}
                  variant="outlined"
                  required
                />
              </Grid>
              <Grid item xs={12} sm={6}>
                <TextField
                  fullWidth
                  label="Last Name"
                  value={prospect.LAST_NAME}
                  onChange={handleInputChange(index, 'LAST_NAME')}
                  InputProps={{
                    startAdornment: (
                      <InputAdornment position="start">
                        <Person />
                      </InputAdornment>
                    ),
                  }}
                  variant="outlined"
                  required
                />
              </Grid>
              <Grid item xs={12}>
                <TextField
                  fullWidth
                  label="Street Address 1"
                  value={prospect.STREET1}
                  onChange={handleInputChange(index, 'STREET1')}
                  InputProps={{
                    startAdornment: (
                      <InputAdornment position="start">
                        <Home />
                      </InputAdornment>
                    ),
                  }}
                  variant="outlined"
                />
              </Grid>
              <Grid item xs={12}>
                <TextField
                  fullWidth
                  label="Street Address 2 (Optional)"
                  value={prospect.STREET2}
                  onChange={handleInputChange(index, 'STREET2')}
                  InputProps={{
                    startAdornment: (
                      <InputAdornment position="start">
                        <Home />
                      </InputAdornment>
                    ),
                  }}
                  variant="outlined"
                />
              </Grid>
              <Grid item xs={12} sm={4}>
                <TextField
                  fullWidth
                  label="City"
                  value={prospect.CITY}
                  onChange={handleInputChange(index, 'CITY')}
                  InputProps={{
                    startAdornment: (
                      <InputAdornment position="start">
                        <LocationCity />
                      </InputAdornment>
                    ),
                  }}
                  variant="outlined"
                />
              </Grid>
              <Grid item xs={12} sm={4}>
                <TextField
                  fullWidth
                  label="State"
                  value={prospect.STATE}
                  onChange={handleInputChange(index, 'STATE')}
                  InputProps={{
                    startAdornment: (
                      <InputAdornment position="start">
                        <Public />
                      </InputAdornment>
                    ),
                  }}
                  variant="outlined"
                  placeholder="TX"
                />
              </Grid>
              <Grid item xs={12} sm={4}>
                <TextField
                  fullWidth
                  label="ZIP Code"
                  value={prospect.ZIP}
                  onChange={handleInputChange(index, 'ZIP')}
                  InputProps={{
                    startAdornment: (
                      <InputAdornment position="start">
                        <MailOutline />
                      </InputAdornment>
                    ),
                  }}
                  variant="outlined"
                  placeholder="12345"
                />
              </Grid>
            </Grid>
          </CardContent>
        </Card>
      ))}
      
      <Box sx={{ display: 'flex', gap: 2, mb: 3 }}>
        <Button
          variant="outlined"
          startIcon={<Add />}
          onClick={addProspect}
          sx={{ minWidth: 150 }}
        >
          Add Prospect
        </Button>
      </Box>
      
      <Box sx={{ display: 'flex', gap: 2, justifyContent: 'flex-end' }}>
        <Button
          type="button"
          variant="outlined"
          startIcon={<Clear />}
          onClick={resetForm}
          size="large"
        >
          Clear All
        </Button>
        <Button
          type="submit"
          variant="contained"
          startIcon={<Search />}
          size="large"
          sx={{ minWidth: 150 }}
        >
          Search All
        </Button>
      </Box>
    </Box>
  );
};

export default SearchForm;