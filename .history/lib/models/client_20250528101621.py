from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from import Base

class Client(Base):
    __tablename__ = 'clients'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String)
    company_name = Column(String)
    phone = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'))

    user = relationship("User", back_populates="clients")
    jobs = relationship("Job", back_populates="client")

    def __repr__(self):
        return f"<Client {self.name}>"
