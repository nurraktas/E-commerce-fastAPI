from fastapi import FastAPI, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from database import SessionLocal, engine, get_db
import Model as model
import Schemas as schemas 
import traceback
from typing import List
from fastapi.responses import JSONResponse
from exceptions import AppException, ProductNotFoundException, CartNotFoundException, OutOfStockException
from routers import products, carts, auth, orders
import hashlib
from passlib.context import CryptContext
from config import settings
from fastapi.middleware.cors import CORSMiddleware

DATABASE_URL = settings.DATABASE_URL
SECRET_KEY = settings.SECRET_KEY

#veritabani tablolari
model.Base.metadata.create_all(bind=engine)

# be app
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173/"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(products.router)
app.include_router(carts.router)
app.include_router(auth.router)
app.include_router(orders.router)




@app.exception_handler(AppException)
async def app_exception_handler(request: Request,exc: AppException):
    return JSONResponse(
       
        status_code=exc.status_code,
        content={"message": "exc.message"}
    )
    



#main page
@app.get("/")
def read_root():
    return{"message": "Welcome to e-commerce API"}


















