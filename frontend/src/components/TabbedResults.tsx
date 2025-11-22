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
  TextField,
  InputAdornment,
  Collapse,
  IconButton,
  Button,
  Alert,
  CircularProgress,
} from '@mui/material';
import {
  Search as SearchIcon,
  Add as AddIcon,
  Remove as RemoveIcon,
  Psychology as PsychologyIcon,
} from '@mui/icons-material';
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
  const [expandedSections, setExpandedSections] = useState<{ [key: string]: boolean }>({});
  const [aiInsightsLoading, setAiInsightsLoading] = useState<{ [key: string]: boolean }>({});
  const [aiInsightsResults, setAiInsightsResults] = useState<{ [key: string]: string }>({});

  const handleChange = (event: React.SyntheticEvent, newValue: number) => {
    setValue(newValue);
  };

  const toggleSection = (sectionKey: string) => {
    setExpandedSections(prev => ({
      ...prev,
      [sectionKey]: !prev[sectionKey]
    }));
  };

  const handleAiInsights = async (category: string) => {
    setAiInsightsLoading(prev => ({ ...prev, [category]: true }));
    
    // Simulate API call delay
    setTimeout(() => {
      setAiInsightsResults(prev => ({ 
        ...prev, 
        [category]: "This feature is still in progress. AI insights will be available soon!" 
      }));
      setAiInsightsLoading(prev => ({ ...prev, [category]: false }));
    }, 2000);
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
      'Profile': [] as Array<[string, any]>,
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
        (lowerKey.includes('health') && lowerKey.includes('cause'))
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
        (lowerKey.includes('estimated') && (lowerKey.includes('home') || lowerKey.includes('value'))) ||
        (lowerKey.includes('property') && lowerKey.includes('value')) ||
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
        categories['Profile'].push([key, value]);
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

  // Define sub-sections for each category
  const getSubSections = (category: string, fields: Array<[string, any]>) => {
    const subSections: { [key: string]: Array<[string, any]> } = {};
    
    switch (category) {
      case 'Profile':
        // Add predefined Overview Section tiles
        subSections['Overview Section'] = [
          ['Lifetime Giving', 'Coming Soon'],
          ['Largest Gift', 'Coming Soon'],
          ['First Gift', 'Coming Soon'],
          ['Latest Gift', 'Coming Soon'],
          ['Overall Score', 'Coming Soon'],
          ['Propensity', 'Coming Soon'],
          ['Capacity', 'Coming Soon'],
          ['Planned Giving', 'Coming Soon'],
          ['Capacity Range $', 'Coming Soon'],
          ['Total Political Giving $', 'Coming Soon'],
          ['Charitable Giving $', 'Coming Soon'],
          ['Estimated Household Income', 'Coming Soon'],
          ['Home Market Value', 'Coming Soon'],
          ['Net Worth', 'Coming Soon']
        ];
        subSections['Giving History'] = [
          ['Gift Date', 'Coming Soon'],
          ['Gift Amount', 'Coming Soon'],
          ['Gift Type', 'Coming Soon'],
          ['Campaign ID', 'Coming Soon'],
          ['Fund ID', 'Coming Soon'],
          ['Appeal', 'Coming Soon'],
          ['Location ID', 'Coming Soon']
        ];
        subSections['Biography'] = [];
        
        fields.forEach(([key, value]) => {
          const lowerKey = key.toLowerCase();
          if (!lowerKey.includes('donation') && !lowerKey.includes('giving') && !lowerKey.includes('charity')) {
            subSections['Biography'].push([key, value]);
          }
        });
        break;
        
      case 'Consumer Behavior':
        subSections['Consumer Behavior'] = fields;
        break;
        
      case 'Financial':
        subSections['Wealth Analysis'] = [];
        subSections['Assets'] = [];
        subSections['Donor Advised Funds'] = [];
        subSections['Foundation-Personal/Public'] = [];
        
        fields.forEach(([key, value]) => {
          const lowerKey = key.toLowerCase();
          if (lowerKey.includes('wealth') || lowerKey.includes('income') || lowerKey.includes('credit')) {
            subSections['Wealth Analysis'].push([key, value]);
          } else if (lowerKey.includes('asset') || lowerKey.includes('property') || lowerKey.includes('home')) {
            subSections['Assets'].push([key, value]);
          } else if (lowerKey.includes('fund') || lowerKey.includes('daf')) {
            subSections['Donor Advised Funds'].push([key, value]);
          } else if (lowerKey.includes('foundation')) {
            subSections['Foundation-Personal/Public'].push([key, value]);
          } else {
            subSections['Wealth Analysis'].push([key, value]);
          }
        });
        break;
        
      case 'Political Interests':
        subSections['FEC Contributions'] = fields;
        break;
        
      case 'Charitable Activities':
        subSections['Charitable Activities'] = [];
        subSections['AI Summary'] = [];
        
        fields.forEach(([key, value]) => {
          const lowerKey = key.toLowerCase();
          if (lowerKey.includes('ai') || lowerKey.includes('summary') || lowerKey.includes('analysis')) {
            subSections['AI Summary'].push([key, value]);
          } else {
            subSections['Charitable Activities'].push([key, value]);
          }
        });
        break;
        

      default:
        subSections['Overview'] = fields;
    }
    
    // Remove empty sub-sections
    Object.keys(subSections).forEach(key => {
      if (subSections[key].length === 0) {
        delete subSections[key];
      }
    });
    
    return subSections;
  };

  // Create expandable sub-section component
  const createExpandableSubSection = (title: string, fields: Array<[string, any]>, sectionKey: string) => {
    const isExpanded = expandedSections[sectionKey];
    
    if (fields.length === 0) return null;

    return (
      <Box key={sectionKey} sx={{ mb: 2 }}>
        <Box
          sx={{
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
            p: 2,
            backgroundColor: '#f8f9fa',
            borderRadius: 1,
            cursor: 'pointer',
            '&:hover': {
              backgroundColor: '#e9ecef',
            }
          }}
          onClick={() => toggleSection(sectionKey)}
        >
          <Typography variant="h6" sx={{ fontWeight: 600, color: '#495057' }}>
            {title}
          </Typography>
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
            <Chip 
              label={fields.length} 
              size="small" 
              color="primary"
              sx={{ fontWeight: 600 }}
            />
            <IconButton size="small" sx={{ color: '#6c757d' }}>
              {isExpanded ? <RemoveIcon /> : <AddIcon />}
            </IconButton>
          </Box>
        </Box>
        
        <Collapse in={isExpanded}>
          <Box sx={{ mt: 1 }}>
            {createResultsTable(fields)}
          </Box>
        </Collapse>
      </Box>
    );
  };

  // Create AI Insights component
  const createAiInsightsSection = (category: string) => {
    const isLoading = aiInsightsLoading[category];
    const result = aiInsightsResults[category];

    return (
      <Box sx={{ mb: 3, p: 2, backgroundColor: '#f8f9fa', borderRadius: 2 }}>
        <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', mb: 2 }}>
          <Typography variant="h6" sx={{ fontWeight: 600, color: '#495057' }}>
            AI Insights
          </Typography>
          <Button
            variant="contained"
            size="small"
            startIcon={isLoading ? <CircularProgress size={16} color="inherit" /> : <PsychologyIcon />}
            onClick={() => handleAiInsights(category)}
            disabled={isLoading}
            sx={{
              backgroundColor: '#6366f1',
              '&:hover': { backgroundColor: '#5b5bd6' }
            }}
          >
            {isLoading ? 'Generating...' : 'Get AI Insights'}
          </Button>
        </Box>
        
        {result && (
          <Alert 
            severity="info" 
            sx={{ 
              backgroundColor: '#e3f2fd',
              border: '1px solid #bbdefb'
            }}
          >
            {result}
          </Alert>
        )}
      </Box>
    );
  };

  // Create the results with expandable sub-sections
  const createExpandableResults = (category: string, fields: Array<[string, any]>) => {
    const hasAiInsights = ['Political Interests', 'Charitable Activities', 'Profile'].includes(category);
    
    if (fields.length === 0) {
      return (
        <Box>
          <Paper variant="outlined" sx={{ p: 6, textAlign: 'center', bgcolor: 'grey.50' }}>
            <Typography variant="h6" color="text.secondary" gutterBottom>
              No data available
            </Typography>
            <Typography variant="body2" color="text.secondary">
              This category doesn't contain any information for the current search result.
            </Typography>
          </Paper>
          {hasAiInsights && createAiInsightsSection(category)}
        </Box>
      );
    }

    const subSections = getSubSections(category, fields);
    
    return (
      <Box>
        {Object.entries(subSections).map(([title, subFields]) => 
          createExpandableSubSection(title, subFields, `${category}-${title}`)
        )}
        {hasAiInsights && createAiInsightsSection(category)}
      </Box>
    );
  };

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
    'Profile',
    'Consumer Behavior',
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
          {createExpandableResults(label, categorizedData[label] || [])}
        </TabPanel>
      ))}
    </Box>
  );
};

export default TabbedResults;