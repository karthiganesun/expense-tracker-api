from sqlalchemy import Column, Integer, String,Float, Numeric,Date
from datetime import datetime
from .database import Base

class User(Base):
    __tablename__ = "Expense_Tracker"

    id = Column(Integer,primary_key=True,index=True)
    title = Column(String,index=True)
    amount = Column(Float,nullable= False,index=True)
    # __table_args__=(CheckConstraints("amount > 0",name="amount_positive_check"))
    category = Column(String,index=True)
    date = Column(Date,index=True)
    notes = Column(String,index=True)