from sqlalchemy import create_engine

from sqlalchemy.orm import sessionmaker

# Setup SQLAlchemy base, engine, and session
Base = declarative_base()
engine = create_engine("sqlite:///freelancer.db")
Session = sessionmaker(bind=engine)
session = Session()

# Import models and enums to make them accessible 
from .user import User
from .client import Client
from .job import Job, JobStatus
from .payment import Payment, PaymentStatus



__all__ = [
    'Base', 'engine', 'Session', 'session',
    'User', 'Client', 'Job', 'Payment',
    'JobStatus', 'PaymentStatus',
]
