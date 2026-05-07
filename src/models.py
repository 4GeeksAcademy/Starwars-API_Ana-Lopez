from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column

db = SQLAlchemy()

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional
from sqlalchemy import Integer
from sqlalchemy import BigInteger
from sqlalchemy import Float
from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column
from typing import Optional
from typing import List
from datetime import date


db = SQLAlchemy()

class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False, default=True)
   
    favorites: Mapped[List["Favorite"]] = relationship(back_populates="user")
    
    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }
    



class Planets(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), unique=False, nullable=False)
    slug: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    climate: Mapped[Optional[str]] = mapped_column(String(120), nullable=True, unique=False)
    terrain: Mapped[Optional[str]] = mapped_column(String(120), nullable=True, unique=False)
    population: Mapped[Optional[int]] = mapped_column(BigInteger, nullable=True, unique=False)
    diameter: Mapped[Optional[int]] = mapped_column(Integer, nullable=True, unique=False)
    rotation_period: Mapped[Optional[int]] = mapped_column(Integer, nullable=True, unique=False)
    orbital_period: Mapped[Optional[int]] = mapped_column(Integer, nullable=True, unique=False)
    gravity: Mapped[Optional[str]] = mapped_column(String(50), nullable=True, unique=False)

    favorites: Mapped[List["Favorite"]] = relationship(back_populates="planet")
   
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "slug": self.slug,
            "climate": self.climate,
            "terrain": self.terrain,
            "population": self.population,
            "diameter": self.diameter,
            "rotation_period": self.rotation_period,
            "orbital_period": self.orbital_period,
            "gravity": self.gravity,
        }

class Character(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    slug: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    gender: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    birth_year: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    height: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    mass: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    hair_color: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    skin_color: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    eye_color: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)

    favorites: Mapped[List["Favorite"]] = relationship(back_populates="character")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "slug": self.slug,
            "gender": self.gender,
            "birth_year": self.birth_year,
            "height": self.height,
            "mass": self.mass,
            "hair_color": self.hair_color,
            "skin_color": self.skin_color,
            "eye_color": self.eye_color,
        }
    
class Favorite(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    planet_id: Mapped[Optional[int]] = mapped_column(ForeignKey("planets.id"), nullable=True)
    character_id: Mapped[Optional[int]] = mapped_column(ForeignKey("character.id"), nullable=True)

    user: Mapped["User"] = relationship(back_populates="favorites")
    character: Mapped[Optional["Character"]] = relationship(back_populates="favorites")
    planet: Mapped[Optional["Planets"]] = relationship(back_populates="favorites")
