from sqlalchemy import Column, Integer, String, ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

from passlib.apps import custom_app_context


Base = declarative_base()

class User(Base):
    """
    Stores user details
    """
    __tablename__ = "user"

    id = Column(Integer, primary_key = True)
    name = Column(String(32), index = True)
    password_hash = Column(String(64), nullable = False)

    def hash_password(self, password):
        self.password_hash = custom_app_context.encrypt(password)

    def verify_password(self, password):
        return custom_app_context.verify(password, self.password_hash)

class Genre(Base):
    """
    List of Anime Genres
    """
    __tablename__ = "genre"
    
    id = Column(Integer, primary_key = True)
    name = Column(String(20), nullable = False)

    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

class Item(Base):
    """
    Stores properties of each Anime
    """
    __tablename__ = "item"

    id = Column(Integer, primary_key = True)
    name = Column(String(30), nullable = False)
    description = Column(String(250))

    genre_id = Column(Integer, ForeignKey('genre.id'))
    genre = relationship(Genre)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)



engine = create_engine("sqlite:///AnimeCatalog.db")
Base.metadata.create_all(engine)