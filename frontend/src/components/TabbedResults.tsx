import React, { useState } from 'react';
import {
  Box,
  Tabs,
  Tab,
  Typography,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  Chip,
  Badge,
  TextField,
  InputAdornment,
} from '@mui/material';
import SearchIcon from '@mui/icons-material/Search';
import { SearchResult } from '../types';

interface TabbedResultsProps {
  data: SearchResult;
}

interface TabPanelProps {
  children?: React.ReactNode;
  index: number;
  value: number;
}

function TabPanel(props: TabPanelProps) {
  const { children, value, index, ...other } = props;

  return (
    <div
      role="tabpanel"
      hidden={value !== index}
      id={`results-tabpanel-${index}`}
      aria-labelledby={`results-tab-${index}`}
      {...other}
    >
      {value === index && <Box sx={{ p: 3 }}>{children}</Box>}
    </div>
  );
}

const TabbedResults: React.FC<TabbedResultsProps> = ({ data }) => {
  const [value, setValue] = useState(0);
  const [searchTerm, setSearchTerm] = useState('');

  const handleChange = (event: React.SyntheticEvent, newValue: number) => {
    setValue(newValue);
  };

  // Helper function to format field names for display
  const formatFieldName = (key: string): string => {
    return key
      .replace(/_/g, ' ')
      .replace(/\b\w/g, l => l.toUpperCase());
  };

  // Helper function to format values for display
  const formatValue = (value: any): React.ReactNode => {
    if (value === null || value === undefined || value === '') {
      return <Typography variant="body2" color="text.secondary">N/A</Typography>;
    }
    
    if (typeof value === 'boolean') {
      return (
        <Chip
          label={value ? 'Yes' : 'No'}
          size="small"
          color={value ? 'success' : 'default'}
          variant="outlined"
        />
      );
    }
    
    if (typeof value === 'object') {
      return (
        <Typography variant="body2" component="pre" sx={{ fontSize: '0.75rem' }}>
          {JSON.stringify(value, null, 2)}
        </Typography>
      );
    }
    
    return <Typography variant="body2">{String(value)}</Typography>;
  };

  // Function to filter fields based on search term
  const filterFields = (fields: Array<[string, any]>, searchTerm: string): Array<[string, any]> => {
    if (!searchTerm.trim()) return fields;
    
    const lowerSearchTerm = searchTerm.toLowerCase();
    return fields.filter(([key, value]) => {
      const keyMatch = key.toLowerCase().includes(lowerSearchTerm);
      const valueMatch = String(value).toLowerCase().includes(lowerSearchTerm);
      return keyMatch || valueMatch;
    });
  };

  // Function to categorize fields based on patterns in field names
  const categorizeFields = (obj: any): Record<string, Array<[string, any]>> => {
    const categories = {
      'Consumer Behavior': [] as Array<[string, any]>,
      'Demographic': [] as Array<[string, any]>,
      'Financial': [] as Array<[string, any]>,
      'Political Interests': [] as Array<[string, any]>,
      'Charitable Activities': [] as Array<[string, any]>,
    };

    const flattenObject = (obj: any, prefix = ''): Array<[string, any]> => {
      const result: Array<[string, any]> = [];
      
      for (const [key, value] of Object.entries(obj)) {
        const displayKey = key;
        
        // Skip empty, null, or undefined values
        if (value === null || value === undefined || value === '' || 
            (Array.isArray(value) && value.length === 0) ||
            (typeof value === 'object' && value !== null && Object.keys(value).length === 0)) {
          continue;
        }
        
        if (typeof value === 'object' && value !== null && !Array.isArray(value)) {
          const nested = flattenObject(value, '');
          result.push(...nested);
        } else {
          result.push([displayKey, value]);
        }
      }
      
      return result;
    };

    const flattenedData = flattenObject(obj);

    // Categorize each field based on keywords in field names
    flattenedData.forEach(([key, value]) => {
      const lowerKey = key.toLowerCase();
      
      // Consumer Behavior patterns
      if (
        lowerKey.includes('acty/int:') ||
        lowerKey.includes('activity') ||
        lowerKey.includes('interest') ||
        lowerKey.includes('hobby') ||
        lowerKey.includes('lifestyle') ||
        lowerKey.includes('truetouch') ||
        lowerKey.includes('behavior') ||
        lowerKey.includes('shopping') ||
        lowerKey.includes('buying') ||
        lowerKey.includes('sports') ||
        lowerKey.includes('music') ||
        lowerKey.includes('travel') ||
        lowerKey.includes('entertainment') ||
        lowerKey.includes('magazine') ||
        lowerKey.includes('reading') ||
        lowerKey.includes('cooking') ||
        lowerKey.includes('crafts') ||
        lowerKey.includes('collecting') ||
        lowerKey.includes('pets') ||
        lowerKey.includes('health/fitness') ||
        lowerKey.includes('fitness') ||
        lowerKey.includes('technology') ||
        lowerKey.includes('electronics') ||
        lowerKey.includes('internet') ||
        lowerKey.includes('computer') ||
        lowerKey.includes('gaming') ||
        lowerKey.includes('video game') ||
        lowerKey.includes('streaming') ||
        lowerKey.includes('outdoor') ||
        lowerKey.includes('recreation') ||
        lowerKey.includes('sweepstakes') ||
        lowerKey.includes('lottery')
      ) {
        categories['Consumer Behavior'].push([key, value]);
      }
      // Political Interests patterns
      else if (
        lowerKey.includes('political') ||
        lowerKey.includes('conservative') ||
        lowerKey.includes('liberal') ||
        lowerKey.includes('voting') ||
        lowerKey.includes('government') ||
        lowerKey.includes('military') ||
        lowerKey.includes('veteran')
      ) {
        categories['Political Interests'].push([key, value]);
      }
      // Charitable Activities patterns
      else if (
        lowerKey.includes('socl caus/con') ||
        lowerKey.includes('social cause') ||
        lowerKey.includes('charitable') ||
        lowerKey.includes('charity') ||
        lowerKey.includes('donation') ||
        lowerKey.includes('donor') ||
        lowerKey.includes('volunteer') ||
        lowerKey.includes('animal wf') ||
        lowerKey.includes('environment') ||
        lowerKey.includes('wildlife') ||
        lowerKey.includes('children') ||
        lowerKey.includes('veterans') ||
        lowerKey.includes('health') && lowerKey.includes('cause')
      ) {
        categories['Charitable Activities'].push([key, value]);
      }
      // Financial patterns
      else if (
        lowerKey.includes('financial') ||
        lowerKey.includes('credit') ||
        lowerKey.includes('invest') ||
        lowerKey.includes('income') ||
        lowerKey.includes('mortgage') ||
        lowerKey.includes('loan') ||
        lowerKey.includes('bank') ||
        lowerKey.includes('equity') ||
        lowerKey.includes('asset') ||
        lowerKey.includes('wealth') ||
        lowerKey.includes('affluence') ||
        lowerKey.includes('estimated') && (lowerKey.includes('home') || lowerKey.includes('value')) ||
        lowerKey.includes('property') && lowerKey.includes('value') ||
        lowerKey.includes('card') ||
        lowerKey.includes('insurance') ||
        lowerKey.includes('retirement') ||
        lowerKey.includes('mutual fund') ||
        lowerKey.includes('stock') ||
        lowerKey.includes('bond') ||
        lowerKey.includes('ira') ||
        lowerKey.includes('money') ||
        lowerKey.includes('payment')
      ) {
        categories['Financial'].push([key, value]);
      }
      // Demographic patterns (everything else demographic-related)
      else if (
        lowerKey.includes('age') ||
        lowerKey.includes('birth') ||
        lowerKey.includes('gender') ||
        lowerKey.includes('marital') ||
        lowerKey.includes('education') ||
        lowerKey.includes('ethnicity') ||
        lowerKey.includes('household') ||
        lowerKey.includes('children') ||
        lowerKey.includes('family') ||
        lowerKey.includes('address') ||
        lowerKey.includes('location') ||
        lowerKey.includes('geography') ||
        lowerKey.includes('dwelling') ||
        lowerKey.includes('homeowner') ||
        lowerKey.includes('renter') ||
        lowerKey.includes('property type') ||
        lowerKey.includes('bedrooms') ||
        lowerKey.includes('year built') ||
        lowerKey.includes('mail') ||
        lowerKey.includes('phone') ||
        lowerKey.includes('email') ||
        lowerKey.includes('person #') ||
        lowerKey.includes('resident') ||
        lowerKey.includes('occupation') ||
        lowerKey.includes('business owner') ||
        lowerKey.includes('new mover')
      ) {
        categories['Demographic'].push([key, value]);
      }
      // Default to Consumer Behavior for unmatched fields
      else {
        categories['Consumer Behavior'].push([key, value]);
      }
    });

    return categories;
  };

  const allCategorizedData = categorizeFields(data);
  
  // Apply search filtering to each category
  const categorizedData = Object.keys(allCategorizedData).reduce((acc, category) => {
    acc[category] = filterFields(allCategorizedData[category], searchTerm);
    return acc;
  }, {} as Record<string, Array<[string, any]>>);

  // Create the results table component
  const createResultsTable = (fields: Array<[string, any]>) => {
    if (fields.length === 0) {
      return (
        <Paper variant="outlined" sx={{ p: 6, textAlign: 'center', bgcolor: 'grey.50' }}>
          <Typography variant="h6" color="text.secondary" gutterBottom>
            No data available
          </Typography>
          <Typography variant="body2" color="text.secondary">
            This category doesn't contain any information for the current search result.
          </Typography>
        </Paper>
      );
    }

    return (
      <TableContainer component={Paper} variant="outlined" sx={{ borderRadius: 2, overflow: 'hidden' }}>
        <Table sx={{ minWidth: 650 }} aria-label="categorized results table">
          <TableHead>
            <TableRow sx={{ 
              backgroundColor: '#283E56',
              '& .MuiTableCell-head': {
                color: 'white',
                fontWeight: 'bold',
              }
            }}>
              <TableCell sx={{ width: '35%', fontSize: '0.875rem' }}>
                Field Name
              </TableCell>
              <TableCell sx={{ width: '65%', fontSize: '0.875rem' }}>
                Value
              </TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {fields.map(([key, value], index) => (
              <TableRow
                key={`${key}-${index}`}
                sx={{
                  '&:nth-of-type(odd)': {
                    backgroundColor: 'grey.50',
                  },
                  '&:hover': {
                    backgroundColor: '#6B7280',
                    transform: 'scale(1.005)',
                    transition: 'all 0.2s ease-in-out',
                    '& .MuiTableCell-root': {
                      color: 'white',
                    }
                  },
                  cursor: 'default',
                }}
              >
                <TableCell 
                  component="th" 
                  scope="row" 
                  sx={{ 
                    fontWeight: 600,
                    fontSize: '0.875rem',
                    borderRight: '1px solid',
                    borderColor: 'divider',
                    verticalAlign: 'top',
                    py: 2,
                  }}
                >
                  {formatFieldName(key)}
                </TableCell>
                <TableCell sx={{ 
                  fontSize: '0.875rem',
                  py: 2,
                  verticalAlign: 'top',
                }}>
                  {formatValue(value)}
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
        <Box sx={{ 
          p: 2, 
          backgroundColor: '#283E56', 
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
        }}>
          <Typography variant="body2" sx={{ color: 'white', fontWeight: 500 }}>
            {fields.length} {fields.length === 1 ? 'field' : 'fields'} with data
          </Typography>
          <Chip 
            label={`${((fields.length / Object.values(allCategorizedData).flat().length) * 100).toFixed(1)}% of total`}
            size="small"
            sx={{ 
              bgcolor: 'white',
              color: '#283E56',
              fontWeight: 600,
            }}
          />
        </Box>
      </TableContainer>
    );
  };

  const tabLabels = [
    'Consumer Behavior',
    'Demographic',
    'Financial',
    'Political Interests', 
    'Charitable Activities'
  ];

  return (
    <Box sx={{ width: '100%' }}>
      {/* Search Field */}
      <Box sx={{ display: 'flex', justifyContent: 'flex-end', mb: 2 }}>
        <TextField
          size="small"
          variant="outlined"
          placeholder="Search results..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          sx={{
            width: 280,
            '& .MuiOutlinedInput-root': {
              backgroundColor: 'white',
              '&:hover fieldset': {
                borderColor: '#283E56',
              },
              '&.Mui-focused fieldset': {
                borderColor: '#283E56',
              },
            },
          }}
          InputProps={{
            startAdornment: (
              <InputAdornment position="start">
                <SearchIcon sx={{ color: '#283E56', fontSize: '1.2rem' }} />
              </InputAdornment>
            ),
          }}
        />
      </Box>
      
      <Paper elevation={1} sx={{ mb: 2 }}>
        <Tabs 
          value={value} 
          onChange={handleChange} 
          aria-label="results categories"
          variant="scrollable"
          scrollButtons="auto"
          sx={{
            '& .MuiTabs-indicator': {
              height: 3,
            },
            '& .MuiTab-root': {
              minHeight: 64,
              textTransform: 'none',
              fontWeight: 600,
              fontSize: '0.875rem',
              '&.Mui-selected': {
                color: 'primary.main',
              },
            },
          }}
        >
          {tabLabels.map((label, index) => {
            const count = categorizedData[label]?.length || 0;
            return (
              <Tab
                key={label}
                label={
                  <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 0.5 }}>
                    <Typography variant="body2" sx={{ fontWeight: 'inherit' }}>
                      {label}
                    </Typography>
                    <Chip 
                      label={count} 
                      size="small" 
                      color={count > 0 ? "primary" : "default"}
                      sx={{ 
                        height: 20, 
                        fontSize: '0.75rem',
                        '& .MuiChip-label': { px: 1 }
                      }}
                    />
                  </Box>
                }
                id={`results-tab-${index}`}
                aria-controls={`results-tabpanel-${index}`}
              />
            );
          })}
        </Tabs>
      </Paper>
      
      {tabLabels.map((label, index) => (
        <TabPanel key={label} value={value} index={index}>
          {createResultsTable(categorizedData[label] || [])}
        </TabPanel>
      ))}
    </Box>
  );
};

export default TabbedResults;