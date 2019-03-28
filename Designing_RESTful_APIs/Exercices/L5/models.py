from sqlalchemy import Column, Boolean, Integer, Float, String, Date, ForeignKey
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from passlib.hash import sha512_crypt

Base = declarative_base()

class User(Base):
    __tablename__= 'user'
    id              = Column(Integer,primary_key=True)
    password_hash   = Column(String(512))
    email           = Column(String, nullable=False)
    user_name       = Column(String, nullable=False, unique=True)
    picture         = Column(String)
    authenticated   = Column(Boolean, default=False)

    def is_authenticated(self):
        return self.authenticated

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    def print_hash(self):
        print(self.password_hash)

    def hash_password(self, password):
        self.password_hash = sha512_crypt.hash(password)

    def verify_password(self, password):
        return sha512_crypt.verify(password, self.password_hash)

    @property
    def serialize(self):
        return dict(id = self.id,
                    user_name = self.user_name,
                    email = self.email)


class MealRequest(Base):
    __tablename__ = 'request'
    id              = Column(Integer, primary_key=True)
    user_id         = Column(Integer, ForeignKey('user.id'))
    meal_type       = Column(String)
    location_name   = Column(String)
    latitude        = Column(Float)
    longitude       = Column(Float)
    appointment_date= Column(Date)
    meal_time       = Column(String)
    match_found     = Column(Boolean)



engine = create_engine('sqlite:///finalProject.db/?check_same_thread=False', echo = True)
Base.metadata.create_all(engine)
