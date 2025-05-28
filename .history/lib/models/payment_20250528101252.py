from sqlalchemy import Column, Integer, ForeignKey, DECIMAL, Date, Enum, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func  
from enum import Enum as PyEnum
from lib.models import Base

class PaymentStatus(PyEnum):
    pending = "pending"
    received = "received"
    overdue = "overdue"

class Payment(Base):
    __tablename__ = 'payments'

    id = Column(Integer, primary_key=True)
    job_id = Column(Integer, ForeignKey('jobs.id'))
    amount = Column(DECIMAL)
    payment_date = Column(Date, default=func.current_date()) 
    status = Column(Enum(PaymentStatus), default=PaymentStatus.pending)
    notes = Column(Text)

    job = relationship("Job", back_populates="payments")

    def __repr__(self):
        return f"<Payment ksh{self.amount} ({self.status.value})>"
