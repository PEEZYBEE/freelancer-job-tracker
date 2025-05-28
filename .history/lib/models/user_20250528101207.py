from sqlalchemy import Column, Integer, String, Text, Date
from sqlalchemy.orm import relationship
from datetime import datetime
from lib. import Base  

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    profile_bio = Column(Text)
    created_at = Column(Date, default=datetime.utcnow)

    jobs = relationship("Job", back_populates="user")
    clients = relationship("Client", back_populates="user", cascade="all, delete-orphan")

    def save(self, session):
        session.add(self)
        session.commit()

    def __repr__(self):
        return f"<User {self.username}>"
