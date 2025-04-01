from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, Integer, ForeignKey, Table, Column 
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()

#table for relationships M <-> M
favorites = Table('favorites', db.Model.metadata,
    Column('user_id', Integer, ForeignKey('user.id'), primary_key=True),
    Column('favorite_id', Integer, nullable=False),
    Column('favorite_type', String(20), nullable=False)  # "planet" or "character"
)

class User(db.Model):
    __tablename__ = 'user'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    #relationships
    favorites: Mapped[list] = relationship("Favorite", back_populates="user")

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            # do not serialize the password, it's a security breach
        }



class Planet(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    uid: Mapped[int] = mapped_column(Integer, unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    climate: Mapped[str] = mapped_column(String(100))
    diameter: Mapped[int] = mapped_column(Integer)
    gravity: Mapped[str] = mapped_column(String(100))
    orbital_period: Mapped[int] = mapped_column(Integer)
    population: Mapped[int] = mapped_column(Integer)
    rotation_period: Mapped[int] = mapped_column(Integer)
    terrain: Mapped[str] = mapped_column(String(100))
    url: Mapped[str] = mapped_column(String(200), nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "uid": self.uid,
            "name": self.name,
            "climate": self.climate,
            "diameter": self.diameter,
            "gravity": self.gravity,
            "orbital_period": self.orbital_period,
            "population": self.population,
            "rotation_period": self.rotation_period,
            "terrain": self.terrain,
            "url": self.url,
        }

class Character(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    uid: Mapped[int] = mapped_column(Integer, unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    gender: Mapped[str] = mapped_column(String(20))
    skin_color: Mapped[str] = mapped_column(String(50))
    hair_color: Mapped[str] = mapped_column(String(50))
    height: Mapped[int] = mapped_column(Integer)
    eye_color: Mapped[str] = mapped_column(String(50))
    mass: Mapped[int] = mapped_column(Integer)
    homeworld: Mapped[str] = mapped_column(String(200))
    birth_year: Mapped[str] = mapped_column(String(20))
    url: Mapped[str] = mapped_column(String(200), nullable=False)
    #relationships
    homeworld: Mapped["Planet"] = relationship("Planet")

    def serialize(self):
        return {
            "id": self.id,
            "uid": self.uid,
            "name": self.name,
            "gender": self.gender,
            "skin_color": self.skin_color,
            "hair_color": self.hair_color,
            "height": self.height,
            "eye_color": self.eye_color,
            "mass": self.mass,
            "homeworld": self.homeworld,
            "birth_year": self.birth_year,
            "url": self.url,
        }

class Favorite(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('user.id'), nullable=False)
    favorite_id: Mapped[int] = mapped_column(Integer, nullable=False)  # ID of either a planet or character
    favorite_type: Mapped[str] = mapped_column(String(20), nullable=False)  # "planet" or "character"

    #relationships
    user: Mapped["User"] = relationship("User", back_populates="favorites")

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "favorite_id": self.favorite_id,
            "favorite_type": self.favorite_type
        }
