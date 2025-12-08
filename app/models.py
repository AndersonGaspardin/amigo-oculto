from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class Group(Base):
    __tablename__ = "groups"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    price = Column(String, nullable=True)
    time = Column(String, nullable=True)
    place = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    participants = relationship("Participant", back_populates="group")
    draws = relationship("Draw", back_populates="group")


class Participant(Base):
    __tablename__ = "participants"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    suggestion = Column(Text)
    secret_token = Column(String, unique=True, nullable=False)
    group_id = Column(Integer, ForeignKey("groups.id"))
    created_at = Column(DateTime, default=datetime.utcnow)

    group = relationship("Group", back_populates="participants")


class Draw(Base):
    __tablename__ = "draws"

    id = Column(Integer, primary_key=True, index=True)
    group_id = Column(Integer, ForeignKey("groups.id"))
    giver_id = Column(Integer, ForeignKey("participants.id"))
    receiver_id = Column(Integer, ForeignKey("participants.id"))

    group = relationship("Group", back_populates="draws")
    giver = relationship("Participant", foreign_keys=[giver_id])
    receiver = relationship("Participant", foreign_keys=[receiver_id])
