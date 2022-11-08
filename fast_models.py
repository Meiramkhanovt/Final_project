from sqlalchemy import Column, Integer, String
from fastDataBase import Base

class Users(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key = True)
    username = Column(String(50), nullable = False, unique = True)
    first_name = Column(String(50), nullable = True)
    last_name = Column(String(50), nullable = True)
    specialization = Column(String(50), nullable = True)
    phone_number = Column(String(50), nullable = True)
    address = Column(String(100), nullable = True)
    email = Column(String(120), nullable = False, unique = True)
    image_file = Column(String(20), nullable = False, default = 'default.jpg')
    password = Column(String(80), nullable = False)