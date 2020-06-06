from sqlalchemy import String, Column, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Character(Base):
    __tablename__ = 'characters'

    id = Column(UUID, primary_key=True)
    user = Column(UUID, ForeignKey('users.id'))
    group = Column(UUID, ForeignKey('groups.id'))
    name = Column(String)

    rel_user = relationship('User')
    rel_group = relationship('Group')
