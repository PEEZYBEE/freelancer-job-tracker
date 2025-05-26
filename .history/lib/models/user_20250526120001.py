from sqlalchemy import Column, Integer, String, Text, Date
from sqlalchemy.orm import relationship
from . import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    profile_bio = Column(Text)
    created_at = Column(Date)

    jobs = relationship("Job", back_populates="user")

    def __repr__(self):
        return f"<User {self.username}>"
