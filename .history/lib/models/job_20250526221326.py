# models/job.py

from sqlalchemy import Column, Integer, String, Text, Date, ForeignKey, Enum
from sqlalchemy.orm import relationship
from enum import Enum as PyEnum
from . import Base

class JobStatus(PyEnum):
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
