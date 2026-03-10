from sqlalchemy import Column, Integer, Float, String, ForeignKey, Boolean
from database import Base
from sqlalchemy.orm import relationship


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(Integer, unique=True, nullable=False)

    products = relationship("Product", back_populates="category")

