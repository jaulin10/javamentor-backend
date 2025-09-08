from sqlalchemy import Column, Integer, String, Text, JSON, Boolean
from app.database import Base


class Exercise(Base):
    __tablename__ = "exercises"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    difficulty = Column(String, nullable=False)  # beginner, intermediate, advanced
    topic = Column(String, nullable=False)  # variables, loops, oop, etc.
    starter_code = Column(Text, nullable=True)
    solution = Column(Text, nullable=True)
    test_cases = Column(JSON, nullable=True)
    is_active = Column(Boolean, default=True)