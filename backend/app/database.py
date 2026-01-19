"""
Database configuration and models using SQLAlchemy
"""

from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean, ForeignKey, Text
from sqlalchemy.dialects.mssql import JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.sql import func
from datetime import datetime, timedelta
import os
from urllib.parse import quote_plus
import hashlib
import json

# Build database URL from individual components 
DB_SERVER = os.getenv("DB_SERVER")
DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_DRIVER = os.getenv("DB_DRIVER")

# Database names -
KC_EXP_DB_DATABASE = os.getenv("KC_EXP_DB_DATABASE")
KC_GT_DB_DATABASE = os.getenv("KC_GT_DB_DATABASE")

# Validate required environment variables
required_vars = {
    "DB_SERVER": DB_SERVER,
    "DB_USERNAME": DB_USERNAME,
    "DB_PASSWORD": DB_PASSWORD,
    "DB_DRIVER": DB_DRIVER,
    "KC_EXP_DB_DATABASE": KC_EXP_DB_DATABASE,
    "KC_GT_DB_DATABASE": KC_GT_DB_DATABASE
}

missing_vars = [var for var, value in required_vars.items() if not value]
if missing_vars:
    raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")

# URL encode the password to handle special characters
encoded_password = quote_plus(DB_PASSWORD) if DB_PASSWORD else ""

# Construct the SQL Server database URLs (using same server/credentials for both)
EXPERIAN_DATABASE_URL = f"mssql+pyodbc://{DB_USERNAME}:{encoded_password}@{DB_SERVER}/{KC_EXP_DB_DATABASE}?driver={quote_plus(DB_DRIVER)}"
GIVINGTREND_DATABASE_URL = f"mssql+pyodbc://{DB_USERNAME}:{encoded_password}@{DB_SERVER}/{KC_GT_DB_DATABASE}?driver={quote_plus(DB_DRIVER)}"

# Create engines for both databases with connection pooling
# pool_recycle=3600 closes idle connections every hour to prevent stale connections causing 0x68 errors
experian_engine = create_engine(EXPERIAN_DATABASE_URL, pool_recycle=3600, pool_pre_ping=True)
givingtrend_engine = create_engine(GIVINGTREND_DATABASE_URL, pool_recycle=3600, pool_pre_ping=True)

ExperianSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=experian_engine)
GivingTrendSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=givingtrend_engine)
Base = declarative_base()

class User(Base):
    """User model for authentication"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    is_active = Column(Boolean, default=True)
    last_login = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=True)
    
    # Relationship to search history
    search_history = relationship("SearchHistory", back_populates="user", cascade="all, delete-orphan")

class SearchHistory(Base):
    """Search history for tracking user searches"""
    __tablename__ = "search_history"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    street = Column(String(255), nullable=True)
    city = Column(String(100), nullable=True)
    state = Column(String(50), nullable=True)
    zip_code = Column(String(20), nullable=True)
    searched_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False, index=True)
    
    # Relationship back to user
    user = relationship("User", back_populates="search_history")

class PasswordResetToken(Base):
    """Password reset token model"""
    __tablename__ = "password_reset_tokens"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    token = Column(String(255), unique=True, index=True, nullable=False)
    expires_at = Column(DateTime(timezone=True), nullable=False)
    used = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationship
    user = relationship("User")

class ExperianAPICache(Base):
    """Cache for Experian API responses with 90-day TTL"""
    __tablename__ = "experian_api_cache"
    
    # Primary key
    id = Column(Integer, primary_key=True, index=True)
    
    # Search criteria - normalized for consistency (based on user input: name + address)
    search_hash = Column(String(64), unique=True, index=True, nullable=False)  # SHA256 hash of normalized criteria
    first_name = Column(String(100), index=True)
    last_name = Column(String(100), index=True)
    address = Column(String(200), index=True)
    city = Column(String(100), index=True)
    state = Column(String(50), index=True)
    zip_code = Column(String(20), index=True)
    
    # API responses stored as JSON
    # search_response: All tabs from main search (Consumer Behavior, Profile, Financial, Political, 
    #                  Charitable, Contact Validation, Philanthropy, Affiliations, Social Media, News)
    search_response = Column(JSON, nullable=False)
    # phone_validation: Response from separate /validate-phone endpoint
    phone_validation = Column(JSON, nullable=True)
    # email_validation: Response from separate /validate-email endpoint
    email_validation = Column(JSON, nullable=True)
    
    # Tracking and cleanup
    api_calls_count = Column(Integer, default=1)  # Number of times this query was made
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False, index=True)
    expires_at = Column(DateTime(timezone=True), nullable=False, index=True)  # 90 days from creation
    last_accessed_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Source tracking
    api_source = Column(String(50), default="experian")  # "experian", "givingtrend", etc.
    
    # Cache statistics
    is_partial = Column(Boolean, default=False)  # True if only partial data available
    error_message = Column(String(500), nullable=True)  # If API returned error


def generate_search_hash(first_name: str = None, last_name: str = None, address: str = None, 
                         city: str = None, state: str = None, zip_code: str = None) -> str:
    """
    Generate a deterministic SHA256 hash from normalized search criteria (name + address).
    Phone and email are NOT included in hash since users don't input those.
    Normalizes input to handle different cases/spacing and create consistent lookups.
    """
    # Normalize inputs - strip whitespace and convert to lowercase
    normalized = {
        'first_name': (first_name or '').strip().lower(),
        'last_name': (last_name or '').strip().lower(),
        'address': (address or '').strip().lower(),
        'city': (city or '').strip().lower(),
        'state': (state or '').strip().lower(),
        'zip_code': (zip_code or '').strip().lower(),
    }
    
    # Create a consistent JSON string for hashing
    hash_input = json.dumps(normalized, sort_keys=True)
    return hashlib.sha256(hash_input.encode()).hexdigest()


def get_cache_expiry_date() -> datetime:
    """Get expiry date for cache (90 days from now)"""
    return datetime.utcnow() + timedelta(days=90)

# Create separate Base for KnowledgeCore database
KCBase = declarative_base()

class Donor(KCBase):
    """Donor model for KnowledgeCore database"""
    __tablename__ = "Donor"
    __table_args__ = {'schema': 'dbo'}
    
    # Primary key
    DonorId = Column(Integer, primary_key=True)
    
    # Parish and identification fields
    ParishIdentifier = Column(String(100))
    ConstituentId = Column(String(100))
    FamilyId = Column(Integer)
    
    # Resident/Primary contact fields
    RELastName = Column(String(100), index=True)
    REMiddleName = Column(String(50))
    REFirstName = Column(String(100), index=True)
    RESpouseId = Column(String(100))
    ReAddress = Column(String(200), index=True)
    RECity = Column(String(100), index=True)
    REZipCode = Column(String(20), index=True)
    REState = Column(String(50), index=True)
    REPhone = Column(String(20))
    REEmail = Column(String(150))
    
    # Parish contact fields
    ParishAddress = Column(String(200))
    ParishLastName = Column(String(100))
    ParishMiddleName = Column(String(50))
    ParishFirstName = Column(String(100))
    ParishCity = Column(String(100))
    ParishState = Column(String(50))
    ParishZipCode = Column(String(20))
    ParishPhone = Column(String(20))
    ParishEmail = Column(String(150))
    
    # Additional fields
    MatchType = Column(String(50))
    REOrgName = Column(String(100))
    RESaluationAddress = Column(String(100))
    RESaluationAddress2 = Column(String(100))
    FundDescription = Column(String(100))


class Constituent(KCBase):
    """Constituent model for KnowledgeCore database"""
    __tablename__ = "Constituent"
    __table_args__ = {'schema': 'dbo'}
    
    # Primary key
    Constituent_ID = Column(String(100), primary_key=True, index=True)
    
    # Campaign and organization
    Campaign_ID = Column(String(100))
    Organization_Name = Column(String(255))
    
    # Name fields
    Title_1 = Column(String(50))
    First_Name = Column(String(100), index=True)
    Last_Name = Column(String(100), index=True)
    Suffix_1 = Column(String(50))
    
    # Addressee and salutation
    Primary_Addressee = Column(String(255))
    Primary_Salutation = Column(String(255))
    
    # Preferred address
    Preferred_Address_Line_1 = Column(String(200), index=True)
    Preferred_Address_Line_2 = Column(String(200))
    Preferred_City = Column(String(100), index=True)
    Preferred_State = Column(String(50), index=True)
    Preferred_ZIP = Column(String(20), index=True)
    
    # Contact information
    Preferred_Home_Phone_Number = Column(String(20))
    Preferred_E_mail_Number = Column(String(150))


class Transaction(KCBase):
    """Transaction model for KnowledgeCore database"""
    __tablename__ = "Transaction"
    __table_args__ = {'schema': 'dbo'}
    
    # Primary key - use Gift_ID or transaction_id if available, otherwise use composite key without amount
    # Removed Gift_Amount from PK to allow multiple transactions with same date and amount
    Constituent_ID = Column(String(100), ForeignKey('dbo.Donor.ConstituentId'), primary_key=True, index=True)
    Gift_Date = Column(DateTime, primary_key=True)
    Gift_Amount = Column(String(50))  # Removed from primary key
    Gift_Type = Column(String(100))
    Gift_Pledge_Balance = Column(String(50))
    
    # Establish relationship to Donor table
    donor = relationship("Donor", foreign_keys=[Constituent_ID])


def get_experian_db():
    """Dependency to get Experian database session"""
    db = ExperianSessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_givingtrend_db():
    """Dependency to get GivingTrend database session"""
    db = GivingTrendSessionLocal()
    try:
        yield db
    finally:
        db.close()
