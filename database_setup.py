from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker


Base = declarative_base()


class Services(Base):
    __tablename__ = "services"
    
    id = Column(Integer, primary_key = True)
    name = Column(String(30), nullable = False)
    description = Column(String(250))

class ServiceItem(Base):
    __tablename__ = "service_item"

    id = Column(Integer, primary_key = True)
    name = Column(String(30), nullable = False)
    description = Column(String(250))

class ServiceItemMenu(Base):
    __tablename__ = "service_item_menu"

    id = Column(Integer, primary_key = True)
    name = Column(String(30), nullable = False)
    description = Column(String(250))


engine = create_engine("sqlite:///ItemCatlog.db")
Base.metadata.create_all(engine)