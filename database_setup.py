from sqlalchemy import Column, Integer, String, ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

from passlib.apps import custom_app_context


Base = declarative_base()

class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key = True)
    name = Column(String(32), index = True)
    password_hash = Column(String(64), nullable = False)

    def hash_password(self, password):
        self.password_hash = custom_app_context.encrypt(password)

    def verify_password(self, password):
        return custom_app_context.verify(password, self.password_hash)

class Services(Base):
    __tablename__ = "services"
    
    id = Column(Integer, primary_key = True)
    name = Column(String(30), nullable = False)
    description = Column(String(250))
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

class ServiceItem(Base):
    __tablename__ = "service_item"

    id = Column(Integer, primary_key = True)
    name = Column(String(30), nullable = False)
    description = Column(String(250))
    service_id = Column(Integer, ForeignKey('services.id'))
    services = relationship(Services)


engine = create_engine("sqlite:///ItemCatalog.db")
Base.metadata.create_all(engine)