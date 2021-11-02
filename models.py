from sqlalchemy.sql.sqltypes import Float
from Sqlite_query import Base
from sqlalchemy import Column, Integer, Float

class Numbers(Base):
    __tablename__ = "numbers"

    id = Column(Integer, primary_key=True, index=True)
    num1 = Column(Float)
    num2 = Column(Float)
    result = Column(Float)