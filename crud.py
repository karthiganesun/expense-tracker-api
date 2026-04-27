from fastapi import FastAPI, HTTPException
from datetime import datetime
from sqlalchemy import extract,func
from sqlalchemy.orm import Session
from . import schemas,models


def createuser(db: Session,user:schemas.UserCreate):

    db_amount = user.amount

    if db_amount < 0:
        raise HTTPException(status_code=422, detail="Amount must be greater than 0")
    else:
        db_user = models.User(title= user.title.lower(), amount= user.amount, category= user.category.lower(),date=datetime.now(),notes= user.notes.lower())
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
    return db_user

def get_expense(db:Session):
    return db.query(models.User).all()
   
def max_expense(db:Session):
    # return db.query(models.User).order_by(models.User.amount.desc()).first()   
    max_amount = db.query(func.max(models.User.amount)
                          ).scalar()
    expense_max = db.query(models.User).filter(models.User.amount == max_amount).first()
    return expense_max

def min_expense(db:Session):
    # return db.query(models.User).order_by(models.User.amount.asc()).first()
    min_amount = db.query(func.min(models.User.amount)
                        ).scalar()
    expense_min = db.query(models.User).filter(models.User.amount == min_amount).first()
    return expense_min 

def get_expensebyid(db:Session,expense_id: int):
    e_id = db.query(models.User).filter(models.User.id==expense_id).first()

    if not e_id:
        raise HTTPException(status_code=404,detail="Expense Id not found")
    else:
        return e_id
    

def get_expensebymonth(db:Session,month: int,year: int):
    # e_month =db.query(models.User).filter(extract('month', models.User.date) == month).all()


    if month<1 or month>12:
        raise HTTPException(status_code=404,detail="invalid month, month between 1 and 12")



    year_data = db.query(models.User).filter(extract('year', models.User.date) == year).first()

    if not year_data:
        raise HTTPException(
            status_code=404,
            detail="Year not found"
        )

    total = (db.query(func.sum(models.User.amount)).filter(extract('month', models.User.date) == month,
    extract('year', models.User.date) == year)
    ).scalar()

    categories = (db.query(models.User.category,func.sum(models.User.amount)).filter(extract('month', models.User.date) == month,
    extract('year', models.User.date) == year).group_by(models.User.category).all())

    breakdown = [
        {"category":category, "amount":amount}
        for category, amount in categories
    ]

    if not total:
        raise HTTPException(status_code=404,detail="month not found in the year")
    else:
        return {"Total_amount":total,
                "category_breakdown": breakdown
                }
    

def update_expense(db:Session,id: int, user:schemas.UserCreate):
    up_expense = db.query(models.User).filter(models.User.id == id).first()

    if not up_expense:
        raise HTTPException(status_code=404, detail="Expense Id is not found")
    else:
        up_expense.title = user.title
        up_expense.amount = user.amount
        up_expense.category = user.category
        up_expense.notes = user.notes

        db.commit()
        db.refresh(up_expense)

    return up_expense    
