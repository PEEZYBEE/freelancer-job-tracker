# models/__init__.py

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Setup SQLAlchemy base, engine, and session
Base = declarative_base()
engine = create_engine("sqlite:///db/freelancer.db")
Session = sessionmaker(bind=engine)
session = Session()

# Import models and enums to make them accessible here
from .user import User
from .client import Client
from .job import Job, JobStatus
from .payment import Payment, PaymentStatus

# Create tables if they don't exist
Base.metadata.create_all(engine)

__all__ = [
    'Base', 'engine', 'Session', 'session',
    'User', 'Client', 'Job', 'Payment',
    'JobStatus', 'PaymentStatus',
]
