from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List, Optional

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "user"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)

    favorite_planets: Mapped[List["FavoritePlanet"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    favorite_people: Mapped[List["FavoritePeople"]] = relationship(back_populates="user", cascade="all, delete-orphan")

    def __repr__(self):
        return f"Usuario: {self.email}"

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
        }

class People(db.Model):
    __tablename__ = "people"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    height: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    mass: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)

    favorites: Mapped[List["FavoritePeople"]] = relationship(back_populates="people", cascade="all, delete-orphan")

    def __repr__(self):
        return f"Personaje: {self.name} (ID: {self.id})"

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "height": self.height,
            "mass": self.mass
        }

class Planet(db.Model):
    __tablename__ = "planet"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    climate: Mapped[Optional[str]] = mapped_column(String(80), nullable=True)
    population: Mapped[Optional[str]] = mapped_column(String(80), nullable=True)

    favorites: Mapped[List["FavoritePlanet"]] = relationship(back_populates="planet", cascade="all, delete-orphan")

    def __repr__(self):
        return f"Planeta: {self.name} (ID: {self.id})"

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "climate": self.climate,
            "population": self.population
        }

class FavoritePlanet(db.Model):
    __tablename__ = "favorite_planet"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    planet_id: Mapped[int] = mapped_column(ForeignKey("planet.id"), nullable=False)

    user: Mapped["User"] = relationship(back_populates="favorite_planets")
    planet: Mapped["Planet"] = relationship(back_populates="favorites")

    def __repr__(self):
        return f"Fav_Planet: User {self.user_id} -> Planet {self.planet_id}"

    def serialize(self):
        return {
            "id": self.id,
            "planet_id": self.planet_id,
            "planet_details": self.planet.serialize() if self.planet else None
        }

class FavoritePeople(db.Model):
    __tablename__ = "favorite_people"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    people_id: Mapped[int] = mapped_column(ForeignKey("people.id"), nullable=False)

    user: Mapped["User"] = relationship(back_populates="favorite_people")
    people: Mapped["People"] = relationship(back_populates="favorites")

    def __repr__(self):
        return f"Fav_People: User {self.user_id} -> People {self.people_id}"

    def serialize(self):
        return {
            "id": self.id,
            "people_id": self.people_id,
            "people_details": self.people.serialize() if self.people else None
        }
