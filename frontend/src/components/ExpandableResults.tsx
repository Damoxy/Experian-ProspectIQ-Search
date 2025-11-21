import React, { useState } from 'react';
import {
  Box,
  Paper,
  Typography,
  Accordion,
  AccordionSummary,
  AccordionDetails,
  Grid,
  Card,
  CardContent,
  Chip,
  IconButton,
  Collapse,
  List,
  ListItem,
  ListItemText,
  Divider,
} from '@mui/material';
import {
  ExpandMore as ExpandMoreIcon,
  Add as AddIcon,
  Remove as RemoveIcon,
} from '@mui/icons-material';
import { SearchResult } from '../types';

interface ExpandableResultsProps {
  data: SearchResult;
}

interface SectionData {
  [key: string]: string | number | boolean | null;
}

interface MainSection {
  title: string;
  color: string;
  subSections: SubSection[];
}

interface SubSection {
  title: string;
  fields: SectionData;
}

const ExpandableResults: React.FC<ExpandableResultsProps> = ({ data }) => {
  const [expandedSections, setExpandedSections] = useState<{ [key: string]: boolean }>({});

  const toggleSection = (sectionKey: string) => {
    setExpandedSections(prev => ({
      ...prev,
      [sectionKey]: !prev[sectionKey]
    }));
  };

  // Define the main sections structure based on your image
  const mainSections: MainSection[] = [
    {
      title: 'Demographic',
      color: '#8E44AD',
      subSections: [
        {
          title: 'Overview Section',
          fields: {
            'Giving Tiles: Lifetime Giving': 'Coming Soon',
            'Giving Tiles: Largest Gift': 'Coming Soon',
            'Giving Tiles: First Gift': 'Coming Soon',
            'Giving Tiles: Latest Gift': 'Coming Soon',
            'Scores: Overall Score': 'Coming Soon',
            'Scores: Propensity': 'Coming Soon',
            'Scores: Capacity': 'Coming Soon',
            'Scores: Planned Giving': 'Coming Soon',
            'Giving Indicators: Capacity Range $': 'Coming Soon',
            'Giving Indicators: Total Political Giving $': 'Coming Soon',
            'Giving Indicators: Charitable Giving $': 'Coming Soon',
            'Wealth Indicators: Estimated Household Income': 'Coming Soon',
            'Wealth Indicators: Home Market Value': 'Coming Soon',
            'Wealth Indicators: Net Worth': 'Coming Soon',
          }
        },
        {
          title: 'Giving History',
          fields: {
            'Total Donations': '$2,500',
            'Frequency': 'Monthly',
            'Last Donation': '2024-10-15',
            'Preferred Causes': 'Education, Health',
            'Donation Method': 'Online',
          }
        },
        {
          title: 'Biography',
          fields: {
            'Profession': data.demographics?.occupation || 'Professional',
            'Years at Address': data.demographics?.yearsAtAddress || 5,
            'Home Ownership': data.demographics?.homeOwnership || 'Owner',
            'Income Range': data.demographics?.incomeRange || '$75,000-$100,000',
            'Credit Rating': 'Excellent',
          }
        }
      ]
    },
    {
      title: 'Consumer Behavior',
      color: '#3498DB',
      subSections: [
        {
          title: 'Consumer Behavior',
          fields: {
            'Shopping Preference': 'Online',
            'Brand Loyalty': 'High',
            'Purchase Frequency': 'Weekly',
            'Avg Transaction': '$125',
            'Preferred Categories': 'Electronics, Books',
          }
        }
      ]
    },
    {
      title: 'Financial',
      color: '#27AE60',
      subSections: [
        {
          title: 'Wealth Analysis',
          fields: {
            'Net Worth': data.financial?.netWorth || '$250,000',
            'Investment Portfolio': '$150,000',
            'Real Estate Value': data.financial?.homeValue || '$350,000',
            'Debt-to-Income': '25%',
            'Credit Score': data.financial?.creditScore || 785,
          }
        },
        {
          title: 'Assets',
          fields: {
            'Primary Residence': data.financial?.homeValue || '$350,000',
            'Investment Accounts': '$125,000',
            'Retirement Savings': '$200,000',
            'Vehicle Value': '$35,000',
            'Other Assets': '$15,000',
          }
        },
        {
          title: 'Donor Advised Funds',
          fields: {
            'DAF Balance': '$50,000',
            'Annual Grants': '$12,000',
            'Preferred Recipients': 'Educational Institutions',
            'Fund Established': '2020',
            'Growth Rate': '8.5%',
          }
        },
        {
          title: 'Foundation-Personal/Public',
          fields: {
            'Foundation Type': 'Private',
            'Assets Under Management': '$500,000',
            'Annual Giving': '$25,000',
            'Focus Areas': 'Education, Environment',
            'Establishment Year': '2018',
          }
        }
      ]
    },
    {
      title: 'Political Interests',
      color: '#E74C3C',
      subSections: [
        {
          title: 'FEC Contributions',
          fields: {
            'Total Contributions': '$5,000',
            'Election Cycles': '2020, 2022, 2024',
            'Party Affiliation': 'Independent',
            'Candidate Support': 'Local/State Level',
            'PAC Contributions': '$1,200',
          }
        },
        {
          title: 'AI Summary',
          fields: {
            'Political Engagement': 'Moderate',
            'Issue Focus': 'Education Policy',
            'Voting History': 'Regular Voter',
            'Advocacy Groups': 'Education Reform Alliance',
            'Social Issues': 'Environmental Protection',
          }
        }
      ]
    },
    {
      title: 'Charitable Activities',
      color: '#F39C12',
      subSections: [
        {
          title: 'AI Summary',
          fields: {
            'Charitable Giving': 'Active Donor',
            'Volunteer Hours': '20 hours/month',
            'Preferred Organizations': 'Local Nonprofits',
            'Giving Pattern': 'Regular, Planned',
            'Board Memberships': 'Community Foundation',
          }
        }
      ]
    }
  ];

  const renderFieldValue = (value: string | number | boolean | null) => {
    if (value === null || value === undefined) return 'N/A';
    if (typeof value === 'boolean') return value ? 'Yes' : 'No';
    return value.toString();
  };

  const renderSubSection = (subSection: SubSection, sectionIndex: number, subIndex: number) => {
    const sectionKey = `${sectionIndex}-${subIndex}`;
    const isExpanded = expandedSections[sectionKey];

    return (
      <Box key={subIndex} sx={{ mb: 2 }}>
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
          <Typography variant="subtitle1" sx={{ fontWeight: 500, color: '#495057' }}>
            {subSection.title}
          </Typography>
          <IconButton size="small" sx={{ color: '#6c757d' }}>
            {isExpanded ? <RemoveIcon /> : <AddIcon />}
          </IconButton>
        </Box>
        
        <Collapse in={isExpanded}>
          <Box sx={{ p: 2, backgroundColor: '#ffffff', border: '1px solid #e9ecef', borderTop: 'none' }}>
            <Grid container spacing={2}>
              {Object.entries(subSection.fields).map(([key, value], fieldIndex) => (
                <Grid item xs={12} sm={6} md={4} key={fieldIndex}>
                  <Card variant="outlined" sx={{ height: '100%' }}>
                    <CardContent sx={{ p: 2 }}>
                      <Typography variant="caption" color="textSecondary" sx={{ fontWeight: 600 }}>
                        {key}
                      </Typography>
                      <Typography variant="body2" sx={{ mt: 1, fontWeight: 500 }}>
                        {renderFieldValue(value)}
                      </Typography>
                    </CardContent>
                  </Card>
                </Grid>
              ))}
            </Grid>
          </Box>
        </Collapse>
      </Box>
    );
  };

  return (
    <Box sx={{ width: '100%' }}>
      <Grid container spacing={3}>
        {mainSections.map((section, sectionIndex) => (
          <Grid item xs={12} key={sectionIndex}>
            <Paper elevation={2} sx={{ overflow: 'hidden' }}>
              {/* Main Section Header */}
              <Box
                sx={{
                  backgroundColor: section.color,
                  color: 'white',
                  p: 2,
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'space-between'
                }}
              >
                <Typography variant="h6" sx={{ fontWeight: 600 }}>
                  {section.title}
                </Typography>
                <Chip
                  label={section.subSections.length}
                  size="small"
                  sx={{
                    backgroundColor: 'rgba(255,255,255,0.2)',
                    color: 'white',
                    fontWeight: 600
                  }}
                />
              </Box>

              {/* Sub Sections */}
              <Box sx={{ p: 2 }}>
                {section.subSections.map((subSection, subIndex) =>
                  renderSubSection(subSection, sectionIndex, subIndex)
                )}
              </Box>
            </Paper>
          </Grid>
        ))}
      </Grid>
    </Box>
  );
};

export default ExpandableResults;