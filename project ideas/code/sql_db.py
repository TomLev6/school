from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)

engine = create_engine('sqlite:///example.db')
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

# Insert a new user
new_user = User(name='John Doe', age=30)
session.add(new_user)
session.commit()

# Query for all users
users = session.query(User).all()
for user in users:
    print(user.id, user.name, user.age)

# Update a user
user_to_update = session.query(User).filter(User.name=='John Doe').first()
user_to_update.age = 31
session.commit()

# Delete a user
user_to_delete = session.query(User).filter(User.name=='John Doe').first()
session.delete(user_to_delete)
session.commit()