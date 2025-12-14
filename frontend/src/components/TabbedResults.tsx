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
  CircularProgress,
} from '@mui/material';
import {
  Search as SearchIcon,
  Add as AddIcon,
  Remove as RemoveIcon,
  Psychology as PsychologyIcon,
} from '@mui/icons-material';
import { SearchResult, SearchFormData } from '../types';
import { validatePhoneNumbers, validateEmailAddress, generateAIInsights } from '../services/api';

interface TabbedResultsProps {
  data: SearchResult;
  searchCriteria?: SearchFormData;
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

const TabbedResults: React.FC<TabbedResultsProps> = ({ data, searchCriteria }) => {
  const [value, setValue] = useState(0);
  const [searchTerm, setSearchTerm] = useState('');
  const [expandedSections, setExpandedSections] = useState<{ [key: string]: boolean }>({});
  const [aiInsightsLoading, setAiInsightsLoading] = useState<{ [key: string]: boolean }>({});
  const [aiInsightsResults, setAiInsightsResults] = useState<{ [key: string]: string }>({});
  const [phoneValidationLoading, setPhoneValidationLoading] = useState(false);
  const [phoneValidationData, setPhoneValidationData] = useState<any>(null);
  const [emailValidationLoading, setEmailValidationLoading] = useState(false);
  const [emailValidationData, setEmailValidationData] = useState<any>(null);

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
    
    try {
      // Create profile data from search criteria and results
      const profileData: any = {};
      
      // Add search criteria (name, city, state) - this is what we need for AI prompts
      if (searchCriteria) {
        profileData.FIRST_NAME = searchCriteria.FIRST_NAME;
        profileData.LAST_NAME = searchCriteria.LAST_NAME;
        profileData.CITY = searchCriteria.CITY;
        profileData.STATE = searchCriteria.STATE;
      }
      
      // Add all available data from the search results
      if (data) {
        Object.keys(data).forEach(key => {
          profileData[key] = data[key];
        });
      }
      
      // Add metadata
      profileData.source = 'Knowledge Core IQ Search';
      profileData.search_timestamp = new Date().toISOString();
      
      console.log(`Generating AI insights for ${category}:`, profileData);
      
      // Call the AI insights API
      const response = await generateAIInsights(category, profileData);
      
      if (response.ai_insights && response.ai_insights.insights) {
        setAiInsightsResults(prev => ({ 
          ...prev, 
          [category]: response.ai_insights.insights
        }));
      } else {
        setAiInsightsResults(prev => ({ 
          ...prev, 
          [category]: "AI insights could not be generated at this time. Please try again later."
        }));
      }
    } catch (error) {
      console.error('AI insights generation failed:', error);
      setAiInsightsResults(prev => ({ 
        ...prev, 
        [category]: `AI insights temporarily unavailable: ${error instanceof Error ? error.message : 'Unknown error'}`
      }));
    } finally {
      setAiInsightsLoading(prev => ({ ...prev, [category]: false }));
    }
  };

  const handlePhoneValidation = async () => {
    if (!searchCriteria) {
      console.warn('No search criteria available for phone validation');
      return;
    }

    setPhoneValidationLoading(true);
    try {
      console.log('Manual phone validation requested...');
      const phoneData = await validatePhoneNumbers(searchCriteria);
      console.log('Raw phone validation response:', phoneData);
      
      if (phoneData && phoneData.phone_validation) {
        console.log('Phone validation data found:', phoneData.phone_validation);
        setPhoneValidationData(phoneData.phone_validation);
        console.log('Phone validation completed');
        
        // Check if there was an error in the response
        if (phoneData.phone_validation.validation_metadata?.error) {
          console.warn('Phone validation API returned error:', phoneData.phone_validation.validation_metadata.error);
        } else {
          console.log('Phone validation successful, total phones:', phoneData.phone_validation.total_phones);
        }
      } else {
        console.warn('No phone_validation data in response:', phoneData);
      }
    } catch (error) {
      console.error('Phone validation request failed:', error);
      
      // Create an error response for display
      setPhoneValidationData({
        phones_found: [],
        mobile_phones: [],
        landline_phones: [],
        dnc_compliant_phones: [],
        non_dnc_phones: [],
        total_phones: 0,
        validation_metadata: {
          error: error instanceof Error ? error.message : 'Network error occurred',
          api_source: 'experian_aperture',
          validation_status: 'network_error'
        }
      });
    } finally {
      setPhoneValidationLoading(false);
    }
  };

  const handleEmailValidation = async () => {
    if (!searchCriteria) {
      console.warn('No search criteria available for email validation');
      return;
    }

    setEmailValidationLoading(true);
    try {
      console.log('Manual email validation requested...');
      const emailData = await validateEmailAddress(searchCriteria);
      console.log('Raw email validation response:', emailData);
      
      if (emailData && emailData.email_validation) {
        console.log('Email validation data found:', emailData.email_validation);
        setEmailValidationData(emailData.email_validation);
        console.log('Email validation completed');
        
        // Check if there was an error in the response
        if (emailData.email_validation.validation_metadata?.error) {
          console.warn('Email validation API returned error:', emailData.email_validation.validation_metadata.error);
        } else {
          console.log('Email validation successful, email found:', emailData.email_validation.email_found);
        }
      } else {
        console.warn('No email_validation data in response:', emailData);
      }
    } catch (error) {
      console.error('Email validation request failed:', error);
      
      // Create an error response for display
      setEmailValidationData({
        email_found: null,
        email_type: null,
        total_emails: 0,
        validation_metadata: {
          error: error instanceof Error ? error.message : 'Network error occurred',
          api_source: 'experian_aperture',
          validation_status: 'network_error'
        }
      });
    } finally {
      setEmailValidationLoading(false);
    }
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
      'Contact Validation': [] as Array<[string, any]>,
      'Philanthropy': [] as Array<[string, any]>,
      'Affiliations': [] as Array<[string, any]>,
      'Social Media': [] as Array<[string, any]>,
      'News': [] as Array<[string, any]>,
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
      
      // Contact Validation patterns (check first to avoid conflicts)
      if (
        lowerKey.includes('phone_validation') ||
        lowerKey.includes('phones_found') ||
        lowerKey.includes('mobile_phones') ||
        lowerKey.includes('landline_phones') ||
        lowerKey.includes('dnc_compliant_phones') ||
        lowerKey.includes('non_dnc_phones') ||
        lowerKey.includes('email_validation') ||
        lowerKey.includes('email_found') ||
        lowerKey.includes('email_type') ||
        lowerKey.includes('validation_metadata') ||
        (lowerKey.includes('phone') && (
          lowerKey.includes('validation') ||
          lowerKey.includes('found') ||
          lowerKey.includes('mobile') ||
          lowerKey.includes('landline') ||
          lowerKey.includes('dnc') ||
          lowerKey.includes('rank') ||
          lowerKey.includes('status')
        )) ||
        (lowerKey.includes('email') && (
          lowerKey.includes('validation') ||
          lowerKey.includes('found') ||
          lowerKey.includes('type')
        ))
      ) {
        categories['Contact Validation'].push([key, value]);
      }
      // Consumer Behavior patterns
      else if (
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

      case 'Contact Validation':
        // Use either the existing phone validation data or manually fetched data
        const phoneValidation = data.phone_validation || phoneValidationData;
        console.log('Contact Validation - data.phone_validation:', data.phone_validation);
        console.log('Contact Validation - phoneValidationData:', phoneValidationData);
        console.log('Contact Validation - final phoneValidation:', phoneValidation);
        
        if (phoneValidation) {
          // Create a single table with all phone validation data
          const allPhones: any[] = [];
          
          // Combine mobile phones
          if (phoneValidation.mobile_phones && phoneValidation.mobile_phones.length > 0) {
            phoneValidation.mobile_phones.forEach((phone: any) => {
              allPhones.push({
                type: 'Mobile',
                number: phone.number,
                dnc_status: phone.dnc_status ? 'Yes' : 'No',
                dnc_date: phone.dnc_date || 'N/A',
                rank: phone.rank
              });
            });
          }
          
          // Combine landline phones
          if (phoneValidation.landline_phones && phoneValidation.landline_phones.length > 0) {
            phoneValidation.landline_phones.forEach((phone: any) => {
              allPhones.push({
                type: 'Landline',
                number: phone.number,
                dnc_status: phone.dnc_status ? 'Yes' : 'No',
                dnc_date: phone.dnc_date || 'N/A',
                rank: phone.rank
              });
            });
          }
          
          // Sort by rank (priority)
          allPhones.sort((a, b) => a.rank - b.rank);
          
          // Store phone data for custom table rendering
          if (allPhones.length > 0) {
            subSections['Phone Numbers'] = [
              ['__PHONE_TABLE__', JSON.stringify(allPhones)]
            ];
          }
          
          // Add validation status if there's an error
          const metadata = phoneValidation.validation_metadata;
          if (metadata && (metadata.error || metadata.validation_status === 'failed' || metadata.validation_status === 'error')) {
            subSections['Validation Status'] = [
              ['Status', 'Error'],
              ['Error Message', metadata.error || 'Unknown error occurred']
            ];
          }
        } else {
          // Show when no phone validation data is available
          subSections['Phone Validation'] = [
            ['Status', 'No phone data found during search'],
            ['Note', 'Phone validation is automatically performed during search']
          ];
        }

        // Email Validation Section
        const emailValidation = data.email_validation || emailValidationData;
        console.log('Contact Validation - emailValidationData:', emailValidationData);
        console.log('Contact Validation - final emailValidation:', emailValidation);
        
        if (emailValidation && emailValidation.emails_found && emailValidation.emails_found.length > 0) {
          // Create a single table with all email validation data
          const allEmails: any[] = [];
          
          emailValidation.emails_found.forEach((email: any) => {
            allEmails.push({
              type: email.type || 'Unknown',
              address: email.address || email,
              rank: email.rank || 0
            });
          });
          
          // Sort by rank (priority)
          allEmails.sort((a, b) => a.rank - b.rank);
          
          // Store email data for custom table rendering
          if (allEmails.length > 0) {
            subSections['Email Addresses'] = [
              ['__EMAIL_TABLE__', JSON.stringify(allEmails)]
            ];
          }
          
          // Add validation status if there's an error
          const metadata = emailValidation.validation_metadata;
          if (metadata && (metadata.error || metadata.validation_status === 'failed' || metadata.validation_status === 'error')) {
            subSections['Validation Status'] = [
              ['Status', 'Error'],
              ['Error Message', metadata.error || 'Unknown error occurred']
            ];
          }
        } else {
          // Show when no email validation data is available
          subSections['Email Validation'] = [
            ['Status', 'No email data found during search'],
            ['Note', 'Email validation is automatically performed during search']
          ];
          
          // Address verification placeholder
          subSections['Address Verification'] = [
            ['Address Validation', 'Coming Soon'],
            ['Address Type', 'Coming Soon']
          ];
        }
        break;

      case 'Philanthropy':
        subSections['Giving Capacity'] = [
          ['Estimated Capacity', 'Coming Soon'],
          ['Giving History', 'Coming Soon'],
          ['Preferred Causes', 'Coming Soon'],
          ['Donor Segment', 'Coming Soon'],
          ['Annual Giving Potential', 'Coming Soon']
        ];
        subSections['Foundation Involvement'] = [
          ['Board Memberships', 'Coming Soon'],
          ['Foundation Donations', 'Coming Soon'],
          ['Grant Making', 'Coming Soon']
        ];
        break;

      case 'Affiliations':
        subSections['Professional Affiliations'] = [
          ['Current Employer', 'Coming Soon'],
          ['Job Title', 'Coming Soon'],
          ['Industry', 'Coming Soon'],
          ['Professional Associations', 'Coming Soon']
        ];
        subSections['Board Memberships'] = [
          ['Current Boards', 'Coming Soon'],
          ['Past Boards', 'Coming Soon'],
          ['Committee Memberships', 'Coming Soon']
        ];
        break;

      case 'Social Media':
        subSections['Social Profiles'] = [
          ['LinkedIn Profile', 'Coming Soon'],
          ['Facebook Profile', 'Coming Soon'],
          ['Twitter Profile', 'Coming Soon'],
          ['Instagram Profile', 'Coming Soon']
        ];
        subSections['Social Insights'] = [
          ['Social Influence Score', 'Coming Soon'],
          ['Network Size', 'Coming Soon'],
          ['Engagement Rate', 'Coming Soon']
        ];
        break;

      case 'News':
        subSections['Recent Mentions'] = [
          ['News Articles', 'Coming Soon'],
          ['Press Releases', 'Coming Soon'],
          ['Awards & Recognition', 'Coming Soon']
        ];
        subSections['Media Coverage'] = [
          ['Publication Frequency', 'Coming Soon'],
          ['Media Sentiment', 'Coming Soon'],
          ['Key Topics', 'Coming Soon']
        ];
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
          <Paper 
            elevation={1}
            sx={{ 
              p: 3,
              backgroundColor: '#f8fffe',
              border: '1px solid #e0f2f1',
              borderRadius: 2
            }}
          >
            <Typography 
              variant="body1" 
              component="div"
              sx={{ 
                whiteSpace: 'pre-wrap',
                lineHeight: 1.6,
                '& p': { mb: 1 },
                fontFamily: 'inherit'
              }}
            >
              {result.split('\n').map((line, index) => {
                // Handle bullet points
                if (line.trim().startsWith('•')) {
                  return (
                    <Box key={index} sx={{ display: 'flex', alignItems: 'flex-start', mb: 1 }}>
                      <Typography component="span" sx={{ mr: 1, fontWeight: 'bold', color: '#1976d2' }}>
                        •
                      </Typography>
                      <Typography component="span" sx={{ fontWeight: 500 }}>
                        {line.trim().substring(1).trim()}
                      </Typography>
                    </Box>
                  );
                }
                // Handle regular paragraphs
                else if (line.trim()) {
                  return (
                    <Typography key={index} paragraph sx={{ mb: 1.5, textAlign: 'justify' }}>
                      {line.trim()}
                    </Typography>
                  );
                }
                // Handle empty lines
                else {
                  return <Box key={index} sx={{ height: '8px' }} />;
                }
              })}
            </Typography>
          </Paper>
        )}
      </Box>
    );
  };

  // Create the results with expandable sub-sections
  const createExpandableResults = (category: string, fields: Array<[string, any]>) => {
    const hasAiInsights = ['Profile', 'Political Interests', 'Charitable Activities', 'Social Media', 'News'].includes(category);
    
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
            {fields.map(([key, value], index) => {
              // Special handling for phone validation table
              if (key === '__PHONE_TABLE__') {
                const phoneData = JSON.parse(value as string);
                return (
                  <React.Fragment key={`phone-table-${index}`}>
                    {/* Phone table headers */}
                    <TableRow sx={{ backgroundColor: '#f5f5f5' }}>
                      <TableCell colSpan={2} sx={{ p: 0, border: 'none' }}>
                        <Table size="small">
                          <TableHead>
                            <TableRow>
                              <TableCell sx={{ 
                                fontWeight: 700, 
                                fontSize: '0.875rem', 
                                py: 1,
                                borderRight: '1px solid #e0e0e0',
                                width: '60px',
                                textAlign: 'center'
                              }}>S/N</TableCell>
                              <TableCell sx={{ 
                                fontWeight: 700, 
                                fontSize: '0.875rem', 
                                py: 1,
                                borderRight: '1px solid #e0e0e0'
                              }}>Phone Type</TableCell>
                              <TableCell sx={{ 
                                fontWeight: 700, 
                                fontSize: '0.875rem', 
                                py: 1,
                                borderRight: '1px solid #e0e0e0'
                              }}>Phone Number</TableCell>
                              <TableCell sx={{ 
                                fontWeight: 700, 
                                fontSize: '0.875rem', 
                                py: 1,
                                borderRight: '1px solid #e0e0e0'
                              }}>DNC Status</TableCell>
                              <TableCell sx={{ 
                                fontWeight: 700, 
                                fontSize: '0.875rem', 
                                py: 1
                              }}>DNC Revised Date</TableCell>
                            </TableRow>
                          </TableHead>
                          <TableBody>
                            {phoneData.map((phone: any, phoneIndex: number) => (
                              <TableRow 
                                key={phoneIndex}
                                sx={{
                                  '&:nth-of-type(odd)': { backgroundColor: 'grey.50' },
                                  '&:hover': { backgroundColor: '#e3f2fd' }
                                }}
                              >
                                <TableCell sx={{ 
                                  fontSize: '0.875rem', 
                                  py: 1,
                                  borderRight: '1px solid #e0e0e0',
                                  textAlign: 'center',
                                  fontWeight: 600,
                                  color: '#666'
                                }}>{phoneIndex + 1}</TableCell>
                                <TableCell sx={{ 
                                  fontSize: '0.875rem', 
                                  py: 1,
                                  borderRight: '1px solid #e0e0e0'
                                }}>{phone.type}</TableCell>
                                <TableCell sx={{ 
                                  fontSize: '0.875rem', 
                                  py: 1, 
                                  fontWeight: 600,
                                  borderRight: '1px solid #e0e0e0'
                                }}>{phone.number}</TableCell>
                                <TableCell sx={{ 
                                  fontSize: '0.875rem', 
                                  py: 1,
                                  color: phone.dnc_status === 'Yes' ? '#d32f2f' : '#2e7d32',
                                  fontWeight: 600,
                                  borderRight: '1px solid #e0e0e0'
                                }}>{phone.dnc_status}</TableCell>
                                <TableCell sx={{ 
                                  fontSize: '0.875rem', 
                                  py: 1 
                                }}>{phone.dnc_date}</TableCell>
                              </TableRow>
                            ))}
                          </TableBody>
                        </Table>
                      </TableCell>
                    </TableRow>
                  </React.Fragment>
                );
              }
              
              // Special handling for validation buttons
              if (key === '__PHONE_VALIDATION_BUTTON__') {
                return (
                  <TableRow key={`phone-validation-${index}`}>
                    <TableCell sx={{ fontWeight: 600, fontSize: '0.875rem', borderRight: '1px solid', borderColor: 'divider' }}>
                      Action Required
                    </TableCell>
                    <TableCell>
                      <Box sx={{ mt: 1 }}>
                        <Button
                          variant="contained"
                          size="small"
                          onClick={handlePhoneValidation}
                          disabled={phoneValidationLoading || !searchCriteria}
                          startIcon={phoneValidationLoading ? <CircularProgress size={16} /> : undefined}
                        >
                          {phoneValidationLoading ? 'Validating...' : 'Validate Phone Numbers'}
                        </Button>
                        {!searchCriteria && (
                          <Typography variant="caption" display="block" color="text.secondary" sx={{ mt: 1 }}>
                            Search criteria not available
                          </Typography>
                        )}
                      </Box>
                    </TableCell>
                  </TableRow>
                );
              }

              // Custom email table rendering
              if (key === '__EMAIL_TABLE__') {
                const emails = JSON.parse(value);
                return (
                  <React.Fragment key={`email-table-${index}`}>
                    <TableRow>
                      <TableCell 
                        colSpan={2} 
                        sx={{ 
                          p: 0,
                          borderBottom: 'none'
                        }}
                      >
                        <Table size="small" sx={{ backgroundColor: '#f8f9fa' }}>
                          <TableHead>
                            <TableRow sx={{ backgroundColor: '#e9ecef' }}>
                              <TableCell sx={{ 
                                fontSize: '0.875rem', 
                                fontWeight: 700, 
                                py: 1.5,
                                borderRight: '1px solid #e0e0e0',
                                textAlign: 'center',
                                width: '60px'
                              }}>S/N</TableCell>
                              <TableCell sx={{ 
                                fontSize: '0.875rem', 
                                fontWeight: 700, 
                                py: 1.5,
                                borderRight: '1px solid #e0e0e0',
                                width: '120px'
                              }}>Email Type</TableCell>
                              <TableCell sx={{ 
                                fontSize: '0.875rem', 
                                fontWeight: 700, 
                                py: 1.5 
                              }}>Email Address</TableCell>
                            </TableRow>
                          </TableHead>
                          <TableBody>
                            {emails.map((email: any, emailIndex: number) => (
                              <TableRow 
                                key={`email-${emailIndex}`}
                                sx={{
                                  '&:nth-of-type(odd)': { backgroundColor: 'grey.50' },
                                  '&:hover': { backgroundColor: '#e3f2fd' }
                                }}
                              >
                                <TableCell sx={{ 
                                  fontSize: '0.875rem', 
                                  py: 1,
                                  borderRight: '1px solid #e0e0e0',
                                  textAlign: 'center',
                                  fontWeight: 600,
                                  color: '#666'
                                }}>{emailIndex + 1}</TableCell>
                                <TableCell sx={{ 
                                  fontSize: '0.875rem', 
                                  py: 1,
                                  borderRight: '1px solid #e0e0e0'
                                }}>{email.type}</TableCell>
                                <TableCell sx={{ 
                                  fontSize: '0.875rem', 
                                  py: 1, 
                                  fontWeight: 600
                                }}>{email.address}</TableCell>
                              </TableRow>
                            ))}
                          </TableBody>
                        </Table>
                      </TableCell>
                    </TableRow>
                  </React.Fragment>
                );
              }
              
              if (key === '__EMAIL_VALIDATION_BUTTON__') {
                return (
                  <TableRow key={`email-validation-${index}`}>
                    <TableCell sx={{ fontWeight: 600, fontSize: '0.875rem', borderRight: '1px solid', borderColor: 'divider' }}>
                      Action Required
                    </TableCell>
                    <TableCell>
                      <Box sx={{ mt: 1 }}>
                        <Button
                          variant="contained"
                          size="small"
                          onClick={handleEmailValidation}
                          disabled={emailValidationLoading || !searchCriteria}
                          startIcon={emailValidationLoading ? <CircularProgress size={16} /> : undefined}
                          sx={{ ml: 1 }}
                        >
                          {emailValidationLoading ? 'Validating...' : 'Validate Email Address'}
                        </Button>
                        {!searchCriteria && (
                          <Typography variant="caption" display="block" color="text.secondary" sx={{ mt: 1 }}>
                            Search criteria not available
                          </Typography>
                        )}
                      </Box>
                    </TableCell>
                  </TableRow>
                );
              }
              
              // Regular table row rendering
              return (
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
              );
            })}
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
    'Charitable Activities',
    'Contact Validation',
    'Philanthropy',
    'Affiliations',
    'Social Media',
    'News'
  ];

  // Define color themes for each tab
  const tabColors = {
    'Profile': { primary: '#1976d2', light: '#e3f2fd', chip: '#1565c0' },
    'Consumer Behavior': { primary: '#388e3c', light: '#e8f5e8', chip: '#2e7d32' },
    'Financial': { primary: '#f57c00', light: '#fff3e0', chip: '#ef6c00' },
    'Political Interests': { primary: '#7b1fa2', light: '#f3e5f5', chip: '#6a1b9a' },
    'Charitable Activities': { primary: '#d32f2f', light: '#ffebee', chip: '#c62828' },
    'Contact Validation': { primary: '#00796b', light: '#e0f2f1', chip: '#00695c' },
    'Philanthropy': { primary: '#5d4037', light: '#efebe9', chip: '#4e342e' },
    'Affiliations': { primary: '#303f9f', light: '#e8eaf6', chip: '#283593' },
    'Social Media': { primary: '#e91e63', light: '#fce4ec', chip: '#c2185b' },
    'News': { primary: '#455a64', light: '#eceff1', chip: '#37474f' }
  };

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
              backgroundColor: tabColors[tabLabels[value] as keyof typeof tabColors]?.primary || '#1976d2',
            },
            '& .MuiTab-root': {
              minHeight: 64,
              textTransform: 'none',
              fontWeight: 600,
              fontSize: '0.875rem',
              transition: 'all 0.3s ease',
              '&:hover': {
                backgroundColor: 'rgba(0, 0, 0, 0.04)',
              },
            },
          }}
        >
          {tabLabels.map((label, index) => {
            const count = categorizedData[label]?.length || 0;
            const colors = tabColors[label as keyof typeof tabColors];
            const isSelected = value === index;
            
            return (
              <Tab
                key={label}
                label={
                  <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 0.5 }}>
                    <Typography 
                      variant="body2" 
                      sx={{ 
                        fontWeight: 'inherit',
                        color: isSelected ? colors.primary : 'inherit'
                      }}
                    >
                      {label}
                    </Typography>
                    <Chip 
                      label={count} 
                      size="small" 
                      sx={{ 
                        height: 20, 
                        fontSize: '0.75rem',
                        backgroundColor: count > 0 ? (isSelected ? colors.primary : colors.light) : '#f5f5f5',
                        color: count > 0 ? (isSelected ? 'white' : colors.chip) : '#9e9e9e',
                        fontWeight: 600,
                        '& .MuiChip-label': { px: 1 }
                      }}
                    />
                  </Box>
                }
                id={`results-tab-${index}`}
                aria-controls={`results-tabpanel-${index}`}
                sx={{
                  '&.Mui-selected': {
                    backgroundColor: colors.light,
                    '& .MuiTabs-indicator': {
                      backgroundColor: colors.primary,
                    }
                  }
                }}
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