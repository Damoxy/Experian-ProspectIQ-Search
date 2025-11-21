-- Create the main users table
CREATE TABLE users (
    id INT IDENTITY(1,1) PRIMARY KEY,
    email NVARCHAR(255) NOT NULL,
    hashed_password NVARCHAR(255) NOT NULL,
    first_name NVARCHAR(50) NOT NULL,
    last_name NVARCHAR(50) NOT NULL,
    is_active BIT DEFAULT 1,
    created_at DATETIME2 DEFAULT GETUTCDATE(),
    updated_at DATETIME2 DEFAULT GETUTCDATE()
);

-- Create unique constraint on email
ALTER TABLE users ADD CONSTRAINT UQ_users_email UNIQUE (email);

-- Create indexes for better performance
CREATE INDEX IX_users_email ON users(email);
CREATE INDEX IX_users_active ON users(is_active);
CREATE INDEX IX_users_created_at ON users(created_at);

-- Optional: Create search_history table for tracking user searches
CREATE TABLE search_history (
    id INT IDENTITY(1,1) PRIMARY KEY,
    user_id INT NOT NULL,
    search_data NVARCHAR(MAX), -- Stores JSON as text
    results_count INT,
    created_at DATETIME2 DEFAULT GETUTCDATE(),
    CONSTRAINT FK_search_history_user_id FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Create indexes for search_history
CREATE INDEX IX_search_history_user_id ON search_history(user_id);
CREATE INDEX IX_search_history_created_at ON search_history(created_at);

-- Create trigger to update updated_at timestamp
CREATE TRIGGER TR_users_updated_at
ON users
AFTER UPDATE
AS
BEGIN
    UPDATE users 
    SET updated_at = GETUTCDATE()
    FROM users u
    INNER JOIN inserted i ON u.id = i.id;
END;