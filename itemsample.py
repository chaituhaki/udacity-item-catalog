from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from database_setup import Base, Genre, Item, User

engine = create_engine("sqlite:///AnimeCatalog.db")

Base.metadata.bind = engine
DBSession = sessionmaker(engine)
session = DBSession()


"""#USER
user = User(name = "Admin", password = "Everything about Home")
session.add(user)
session.commit()

user = User(name = "Admin1", password = "Home")
session.add(user)
session.commit()
"""



#Services
genre = Genre(name = "Action", user_id = 1)
session.add(genre)
session.commit()

genre = Genre(name = "Adventure", user_id = 2)
session.add(genre)
session.commit()

genre = Genre(name = "Comedy", user_id = 1)
session.add(genre)
session.commit()

genre = Genre(name = "Drama", user_id = 2)
session.add(genre)
session.commit()

genre = Genre(name = "Game", user_id = 1)
session.add(genre)
session.commit()

genre = Genre(name = "Horror", user_id = 2)
session.add(genre)
session.commit()

genre = Genre(name = "Magic", user_id = 1)
session.add(genre)
session.commit()

genre = Genre(name = "Mystery", user_id = 2)
session.add(genre)
session.commit()

genre = Genre(name = "Sci-Fi", user_id = 1)
session.add(genre)
session.commit()

genre = Genre(name = "Shounen", user_id = 2)
session.add(genre)
session.commit()

genre = Genre(name = "Supernatural", user_id = 1)
session.add(genre)
session.commit()



# list 1
item = Item(name = "One Piece", 
                            description = "Pirates Fantasy",
                            genre_id = 1, user_id = 1)
session.add(item)
session.commit()

item = Item(name = "Naruto Shippuden", 
                            description = "Ninja's Never give up",
                            genre_id = 1, user_id = 2)
session.add(item)
session.commit()

item = Item(name = "Hunter X Hunter(2011)", 
                            description = "story runs around Nen",
                            genre_id = 1, user_id = 1)
session.add(item)
session.commit()

item = Item(name = "One Punch Man", 
                            description = "Only one punch is enough to end any enemy",
                            genre_id = 1, user_id = 2)
session.add(item)
session.commit()

item = Item(name = "Gintama", 
                            description = "Samurai world with Aliens",
                            genre_id = 1, user_id = 1)
session.add(item)
session.commit()


item = Item(name = "Attack On Titan", 
                            description = "No words to say",
                            genre_id = 1, user_id = 1)
session.add(item)
session.commit()





# list 2

item = Item(name = "One Piece", 
                            description = "Pirates Fantasy",
                            genre_id = 2, user_id = 1)
session.add(item)
session.commit()


item = Item(name = "Hunter X Hunter(2011)",
                            description = "story runs around Nen",
                            genre_id = 2, user_id = 1)
session.add(item)
session.commit()

item = Item(name = "Naruto Shippuden", 
                            description = "Ninja's Never give up",
                            genre_id = 2, user_id = 2)
session.add(item)
session.commit()

item = Item(name = "Fairy Tail", 
                            description = "Mages can use magic",
                            genre_id = 2, user_id = 2)
session.add(item)
session.commit()

item = Item(name = "Gintama", 
                            description = "Samurai world with Aliens",
                            genre_id = 2, user_id = 1)
session.add(item)
session.commit()


item = Item(name = "Hit Man Reborn", 
                            description = "Mafia",
                            genre_id = 2, user_id = 1)
session.add(item)
session.commit()




# list 3
item = Item(name = "Gintama", 
                            description = "Samurai world with Aliens",
                            genre_id = 3, user_id = 2)
session.add(item)
session.commit()


item = Item(name = "One Punch Man", 
                            description = "Only one punch is enough to end any enemy",
                            genre_id = 3, user_id = 2)
session.add(item)
session.commit()