-- Migration: Create ExperianAPICache table for caching Experian API responses
-- Purpose: Cache API responses with 90-day TTL to reduce API calls and improve performance
-- Database: KC_EXP_DB (Experian database)

-- Create the experian_api_cache table
CREATE TABLE [dbo].[experian_api_cache] (
    [id] INT PRIMARY KEY IDENTITY(1,1) NOT NULL,
    
    -- Search criteria fields (normalized) - based on user input: name + address
    [search_hash] VARCHAR(64) UNIQUE NOT NULL,
    [first_name] VARCHAR(100),
    [last_name] VARCHAR(100),
    [address] VARCHAR(200),
    [city] VARCHAR(100),
    [state] VARCHAR(50),
    [zip_code] VARCHAR(20),
    
    -- API response data stored as JSON
    [search_response] NVARCHAR(MAX) NOT NULL,   -- Complete search response with all tabs (Consumer Behavior, Profile, Financial, Political, Charitable, Contact Validation, Philanthropy, Affiliations, Social Media, News)
    [phone_validation] NVARCHAR(MAX),           -- Phone validation response from separate /validate-phone endpoint
    [email_validation] NVARCHAR(MAX),           -- Email validation response from separate /validate-email endpoint
    
    -- Tracking and cleanup
    [api_calls_count] INT DEFAULT 1 NOT NULL,
    [created_at] DATETIME2(7) DEFAULT GETUTCDATE() NOT NULL,
    [expires_at] DATETIME2(7) NOT NULL,     -- 90 days from creation
    [last_accessed_at] DATETIME2(7) DEFAULT GETUTCDATE(),
    
    -- Source tracking
    [api_source] VARCHAR(50) DEFAULT 'experian' NOT NULL,
    
    -- Cache statistics
    [is_partial] BIT DEFAULT 0 NOT NULL,
    [error_message] VARCHAR(500)
);

-- Create indexes for optimal query performance
CREATE NONCLUSTERED INDEX [IX_search_hash] ON [dbo].[experian_api_cache]([search_hash]);
CREATE NONCLUSTERED INDEX [IX_expires_at] ON [dbo].[experian_api_cache]([expires_at]);  -- For cleanup queries
CREATE NONCLUSTERED INDEX [IX_created_at] ON [dbo].[experian_api_cache]([created_at]);
CREATE NONCLUSTERED INDEX [IX_last_name_first_name] ON [dbo].[experian_api_cache]([last_name], [first_name]);

-- Add composite index for common search scenarios (last_name + zip_code)
CREATE NONCLUSTERED INDEX [IX_search_criteria] ON [dbo].[experian_api_cache]([last_name], [zip_code]);

-- Create statistics for query optimization
CREATE STATISTICS [STAT_search_hash] ON [dbo].[experian_api_cache]([search_hash]);
CREATE STATISTICS [STAT_expires_at] ON [dbo].[experian_api_cache]([expires_at]);
