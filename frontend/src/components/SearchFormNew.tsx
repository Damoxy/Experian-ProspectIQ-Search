import React, { useState } from 'react';
import {
  Grid,
  TextField,
  Button,
  Box,
  InputAdornment,
  Typography,
  IconButton,
  Divider,
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
        <Card 
          key={index} 
          elevation={2} 
          sx={{ 
            mb: 3, 
            borderRadius: 2,
            border: '1px solid',
            borderColor: 'grey.200'
          }}
        >
          <CardContent>
            <Box display="flex" justifyContent="space-between" alignItems="center" mb={2}>
              <Typography variant="h6" color="primary.main">
                Prospect #{index + 1}
              </Typography>
              <Box>
                {prospects.length > 1 && (
                  <IconButton
                    onClick={() => removeProspect(index)}
                    color="error"
                    size="small"
                  >
                    <Delete />
                  </IconButton>
                )}
                {index === prospects.length - 1 && (
                  <IconButton
                    onClick={addProspect}
                    color="primary"
                    size="small"
                  >
                    <Add />
                  </IconButton>
                )}
              </Box>
            </Box>

            <Grid container spacing={2}>
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
                  size="small"
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
                  size="small"
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
                  size="small"
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
                  size="small"
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
                  size="small"
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
                  size="small"
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
                  size="small"
                  placeholder="12345"
                />
              </Grid>
            </Grid>
          </CardContent>
        </Card>
      ))}

      <Divider sx={{ my: 3 }} />
      
      <Box display="flex" justifyContent="space-between" alignItems="center">
        <Button
          startIcon={<Add />}
          onClick={addProspect}
          variant="outlined"
          size="large"
        >
          Add Another Prospect
        </Button>
        
        <Box display="flex" gap={2}>
          <Button
            type="button"
            variant="outlined"
            onClick={resetForm}
            size="large"
            startIcon={<Clear />}
          >
            Clear All
          </Button>
          <Button
            type="submit"
            variant="contained"
            size="large"
            startIcon={<Search />}
            sx={{ minWidth: 150 }}
          >
            Search Prospects
          </Button>
        </Box>
      </Box>
    </Box>
  );
};

export default SearchForm;