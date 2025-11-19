import React, { useState } from 'react';
import {
  Grid,
  TextField,
  Button,
  Box,
  InputAdornment,
} from '@mui/material';
import {
  Person,
  Home,
  LocationCity,
  Public,
  MailOutline,
} from '@mui/icons-material';
import { SearchFormData } from '../types';

interface SearchFormProps {
  onSubmit: (data: SearchFormData) => void;
}

const SearchForm: React.FC<SearchFormProps> = ({ onSubmit }) => {
  const [formData, setFormData] = useState<SearchFormData>({
    FIRST_NAME: '',
    LAST_NAME: '',
    STREET1: '',
    STREET2: '',
    CITY: '',
    STATE: '',
    ZIP: '',
  });

  const handleInputChange = (field: keyof SearchFormData) => (
    event: React.ChangeEvent<HTMLInputElement>
  ) => {
    setFormData(prev => ({
      ...prev,
      [field]: event.target.value,
    }));
  };

  const handleSubmit = (event: React.FormEvent) => {
    event.preventDefault();
    onSubmit(formData);
  };

  const resetForm = () => {
    setFormData({
      FIRST_NAME: '',
      LAST_NAME: '',
      STREET1: '',
      STREET2: '',
      CITY: '',
      STATE: '',
      ZIP: '',
    });
  };

  return (
    <Box component="form" onSubmit={handleSubmit}>
      <Grid container spacing={2}>
        <Grid item xs={12}>
          <TextField
            fullWidth
            label="First Name"
            value={formData.FIRST_NAME}
            onChange={handleInputChange('FIRST_NAME')}
            InputProps={{
              startAdornment: (
                <InputAdornment position="start">
                  <Person />
                </InputAdornment>
              ),
            }}
            variant="outlined"
            size="small"
          />
        </Grid>
        <Grid item xs={12}>
          <TextField
            fullWidth
            label="Last Name"
            value={formData.LAST_NAME}
            onChange={handleInputChange('LAST_NAME')}
            InputProps={{
              startAdornment: (
                <InputAdornment position="start">
                  <Person />
                </InputAdornment>
              ),
            }}
            variant="outlined"
            size="small"
            required
          />
        </Grid>
        <Grid item xs={12}>
          <TextField
            fullWidth
            label="Street Address 1"
            value={formData.STREET1}
            onChange={handleInputChange('STREET1')}
            InputProps={{
              startAdornment: (
                <InputAdornment position="start">
                  <Home />
                </InputAdornment>
              ),
            }}
            variant="outlined"
            size="small"
          />
        </Grid>
        <Grid item xs={12}>
          <TextField
            fullWidth
            label="Street Address 2 (Optional)"
            value={formData.STREET2}
            onChange={handleInputChange('STREET2')}
            InputProps={{
              startAdornment: (
                <InputAdornment position="start">
                  <Home />
                </InputAdornment>
              ),
            }}
            variant="outlined"
            size="small"
          />
        </Grid>
        <Grid item xs={12}>
          <TextField
            fullWidth
            label="City"
            value={formData.CITY}
            onChange={handleInputChange('CITY')}
            InputProps={{
              startAdornment: (
                <InputAdornment position="start">
                  <LocationCity />
                </InputAdornment>
              ),
            }}
            variant="outlined"
            size="small"
          />
        </Grid>
        <Grid item xs={12}>
          <TextField
            fullWidth
            label="State"
            value={formData.STATE}
            onChange={handleInputChange('STATE')}
            InputProps={{
              startAdornment: (
                <InputAdornment position="start">
                  <Public />
                </InputAdornment>
              ),
            }}
            variant="outlined"
            size="small"
            placeholder="TX"
          />
        </Grid>
        <Grid item xs={12}>
          <TextField
            fullWidth
            label="ZIP Code"
            value={formData.ZIP}
            onChange={handleInputChange('ZIP')}
            InputProps={{
              startAdornment: (
                <InputAdornment position="start">
                  <MailOutline />
                </InputAdornment>
              ),
            }}
            variant="outlined"
            size="small"
            placeholder="12345"
          />
        </Grid>
      </Grid>
      
      <Box sx={{ mt: 3, display: 'flex', flexDirection: 'column', gap: 1 }}>
        <Button
          type="submit"
          variant="contained"
          fullWidth
          sx={{ py: 1.5 }}
        >
          Search
        </Button>
        <Button
          type="button"
          variant="outlined"
          onClick={resetForm}
          fullWidth
          size="small"
        >
          Clear Form
        </Button>
      </Box>
    </Box>
  );
};

export default SearchForm;