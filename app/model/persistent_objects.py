"""This module define all models (persistent objects) of application. Each model
is a subclasse of the Base class (declarative) from app.model.database module.
The declarative extension in SQLAlchemy allows to define tables and models in one go,
that is in the same class.
"""


from sqlalchemy import Column, Integer, String
from app.model.database import Base


class User(Base):
    """ User's model class.

    Column:
        id (interger, primary key): auto generated by sqlalchemy
        email (string): max-length:50, unique
        name (string): max-length:120, unique

    Attributes:
        name (str): Name of the user.
        email (str): email of the user.
    """

    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    email = Column(String(120), unique=True)

    def __init__(self, name: str = None, email: str = None) -> None:
        """ The constructor for User class.

        Parameters:
            name (str): Name of the user.
            email (str): email of the user.
        """

        self.name = name
        self.email = email

    def __repr__(self) -> str:
        return '<User %r>' % (self.name)
