import React from 'react';
import {
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  Typography,
  Chip,
  Box,
} from '@mui/material';
import { SearchResult } from '../types';

interface ResultsTableProps {
  data: SearchResult;
}

const ResultsTable: React.FC<ResultsTableProps> = ({ data }) => {
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

  // Function to flatten nested objects and collect non-empty values
  const flattenObject = (obj: any, prefix = ''): Array<[string, any]> => {
    const result: Array<[string, any]> = [];
    
    for (const [key, value] of Object.entries(obj)) {
      // Use the key as-is from backend (already mapped to display names)
      const displayKey = key;
      
      // Skip empty, null, or undefined values
      if (value === null || value === undefined || value === '' || 
          (Array.isArray(value) && value.length === 0) ||
          (typeof value === 'object' && value !== null && Object.keys(value).length === 0)) {
        continue;
      }
      
      if (typeof value === 'object' && value !== null && !Array.isArray(value)) {
        // Recursively flatten nested objects
        const nested = flattenObject(value, '');
        result.push(...nested);
      } else {
        result.push([displayKey, value]);
      }
    }
    
    return result;
  };

  const flattenedData = flattenObject(data);

  if (flattenedData.length === 0) {
    return (
      <Box sx={{ p: 3, textAlign: 'center' }}>
        <Typography variant="h6" color="text.secondary">
          No data found in the response
        </Typography>
      </Box>
    );
  }

  return (
    <TableContainer component={Paper} variant="outlined">
      <Table sx={{ minWidth: 650 }} aria-label="search results table">
        <TableHead>
          <TableRow sx={{ backgroundColor: 'grey.50' }}>
            <TableCell sx={{ fontWeight: 'bold', width: '30%' }}>
              Field
            </TableCell>
            <TableCell sx={{ fontWeight: 'bold', width: '70%' }}>
              Value
            </TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {flattenedData.map(([key, value], index) => (
            <TableRow
              key={`${key}-${index}`}
              sx={{
                '&:nth-of-type(odd)': {
                  backgroundColor: 'action.hover',
                },
                '&:hover': {
                  backgroundColor: 'action.selected',
                },
              }}
            >
              <TableCell component="th" scope="row" sx={{ fontWeight: 500 }}>
                {formatFieldName(key)}
              </TableCell>
              <TableCell>
                {formatValue(value)}
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
      <Box sx={{ p: 2, backgroundColor: 'grey.50', textAlign: 'center' }}>
        <Typography variant="caption" color="text.secondary">
          Showing {flattenedData.length} fields with data
        </Typography>
      </Box>
    </TableContainer>
  );
};

export default ResultsTable;