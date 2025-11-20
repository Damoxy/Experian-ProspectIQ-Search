"""
Database configuration and models using SQLAlchemy
"""

from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.sql import func
from datetime import datetime
import os
from urllib.parse import quote_plus

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

# Create engines for both databases
experian_engine = create_engine(EXPERIAN_DATABASE_URL)
givingtrend_engine = create_engine(GIVINGTREND_DATABASE_URL)

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
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

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

