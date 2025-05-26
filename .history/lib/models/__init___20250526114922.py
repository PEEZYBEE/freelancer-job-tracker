from sqlalchemy import create_engine, Column, Integer, String, Text, Date, ForeignKey, DECIMAL, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
import enum
from datetime import datetime

Base = declarative_base()
engine = create_engine("sqlite:///db/freelancer.db")
Session = sessionmaker(bind=engine)
session = Session()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    profile_bio = Column(Text)
    created_at = Column(Date, default=datetime.utcnow)

    jobs = relationship("Job", back_populates="user")

    def __repr__(self):
        return f"<User {self.username}>"


class Client(Base):
    __tablename__ = 'clients'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String)
    company_name = Column(String)
    phone = Column(String)
    notes = Column(Text)

    jobs = relationship("Job", back_populates="client")

    def __repr__(self):
        return f"<Client {self.name}>"


class JobStatus(enum.Enum):
    applied = "applied"
    interviewed = "interviewed"
    hired = "hired"
    rejected = "rejected"


class Job(Base):
    __tablename__ = 'jobs'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    client_id = Column(Integer, ForeignKey('clients.id'))
    title = Column(String)
    description = Column(Text)
    platform = Column(String)
    applied_date = Column(Date)
    status = Column(Enum(JobStatus), default=JobStatus.applied)

    user = relationship("User", back_populates="jobs")
    client = relationship("Client", back_populates="jobs")
    payments = relationship("Payment", back_populates="job")

    def __repr__(self):
        return f"<Job {self.title} ({self.status.value})>"


class PaymentStatus(enum.Enum):
    pending = "pending"
    received = "received"
    overdue = "overdue"


class Payment(Base):
    __tablename__ = 'payments'

    id = Column(Integer, primary_key=True)
    job_id = Column(Integer, ForeignKey('jobs.id'))
    amount = Column(DECIMAL)
    payment_date = Column(Date)
    status = Column(Enum(PaymentStatus), default=PaymentStatus.pending)
    notes = Column(Text)

    job = relationship("Job", back_populates="payments")

    def __repr__(self):
        return f"<Payment ${self.amount} ({self.status.value})>"


# Create all tables in the database
Base.metadata.create_all(engine)

# Exported symbols
__all__ = ['Base', 'engine', 'Session', 'session', 'User', 'Client', 'Job', 'Payment', 'JobStatus', 'PaymentStatus']
