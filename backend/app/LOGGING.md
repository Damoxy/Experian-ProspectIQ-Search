# Logging System

## Log Files Location
All logs are stored in: `backend/logs/`

## Log Files Generated
- `experian_api_YYYYMMDD.log` - All application logs (INFO and above)
- `experian_errors_YYYYMMDD.log` - Error logs only (ERROR and above)

## Log Levels
- **DEBUG**: Detailed information for debugging (only when DEBUG=True)
- **INFO**: General information about application flow
- **WARNING**: Something unexpected happened but the application is still working
- **ERROR**: A serious problem occurred
- **CRITICAL**: A very serious error occurred

## What Gets Logged

### API Requests & Responses
- Incoming API requests with parameters
- API response status and size
- Processing time for each request

### Experian API Integration
- Outbound requests to Experian API
- Experian API responses and timing
- Request/response payload sizes

### Data Processing
- Data cleaning and transformation stages
- Input vs output record counts
- Field mapping operations

### Errors
- All exceptions with full stack traces
- Context information about when/where errors occurred
- API error responses

### Application Lifecycle
- Application startup/shutdown
- Configuration loaded
- Server status

## Log Rotation
- Log files are automatically rotated when they reach 10MB
- Up to 5 backup files are kept
- Error logs are rotated at 5MB with 3 backups

## Debug Mode
When `DEBUG=True` in your environment:
- More detailed logging is enabled
- Debug level messages are shown in console
- Additional field mapping details are logged

## Monitoring Tips
1. **Check error logs first** when troubleshooting issues
2. **Use timestamps** to correlate issues with user reports  
3. **Monitor file sizes** - large log files may indicate issues
4. **Look for patterns** in error messages for systemic problems

## Example Log Entries

```
2025-11-17 15:30:25 - INFO - API Request - Endpoint: /search
2025-11-17 15:30:25 - INFO - Experian API Request - Payload size: 1024 bytes
2025-11-17 15:30:26 - INFO - Experian API Response - Status: 200, Size: 5120 bytes, Time: 0.85s
2025-11-17 15:30:26 - DEBUG - Data Processing - Stage: cleaning, Input: 15 items, Output: 12 items
2025-11-17 15:30:26 - INFO - Search completed successfully in 1.02 seconds
```