from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session

from . import models, schemas, crud
from .database import engine,get_db

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

@app.post("/users_expense/", response_model=schemas.UserResponse)
def createuser(user:schemas.UserCreate,db:Session=Depends(get_db)):
    return crud.createuser(db,user)

@app.get("/display_expense/", response_model=list[schemas.UserResponse])
def read_user(db:Session=Depends(get_db)):
    return crud.get_expense(db)

@app.get("/display_maxexpense/", response_model=schemas.UserResponse)
def read_max(db:Session=Depends(get_db)):
    return crud.max_expense(db)

@app.get("/display_minexpense/", response_model=schemas.UserResponse)
def read_min(db:Session=Depends(get_db)):
    return crud.min_expense(db)

@app.get("/getby_id/{expense_id}",response_model=schemas.UserResponse)
def readby_id(expense_id:int, db:Session=Depends(get_db)):
    return crud.get_expensebyid(db, expense_id)


@app.get("/getby_month/",response_model=schemas.ExpenseResponse)
def readby_month(month: int, year: int, db:Session=Depends(get_db)):
    return crud.get_expensebymonth(db,month,year)

@app.put("/update/{expense_id}")
def upd_expense(id: int,user: schemas.UserCreate, db: Session=Depends(get_db)):
    return crud.update_expense(db,id,user)

@app.delete("/delete/{expense_id}")
def delete_expense(id:int,db:Session=Depends(get_db)):
    return crud.delete_user(db,id)