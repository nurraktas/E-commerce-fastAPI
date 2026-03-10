from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import Model as model
import Schemas as schemas
from database import get_db
from exceptions import ProductNotFoundException
from routers import auth
from routers.auth import admin_required


router = APIRouter(
    prefix="/products",
    tags=["Products"]
)

#=======================================================
#URUNLERI LISTELEME
#=======================================================

@router.get("/", response_model=List[schemas.Product])
def read_products(db: Session =Depends(get_db)):
    all_products = db.query(model.Product).all()
    return all_products
    



#========================================================
# URUN EKLEME
#========================================================
@router.post("/", response_model=schemas.Product)
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db), current_user: model.User = Depends(auth.admin_required)):
    db_product = model.Product(
        name = product.name,
        description = product.description,
        price = product.price,
        stock = product.stock,
        category = product.category

    )

    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


#============================================================
#URUN BILGILERINI GUNCELLEME
#============================================================
@router.put("/{product_id}", response_model= schemas.Product)
def update_product(product_id: int, update_product: schemas.ProductCreate, db: Session= Depends(get_db), current_user: int= Depends(auth.get_current_user)):
   print(f"Product updated: Id {product_id}")

   db_product = db.query(model.Product).filter(model.Product.id == product_id).first()

   if not db_product:
     raise ProductNotFoundException()

   db_product.name = update_product.name
   db_product.description = update_product.description
   db_product.price = update_product.price
   db_product.stock = update_product.stock
   db_product.category = update_product.category

   db.commit()

   db.refresh(db_product)
   return db_product


#=======================================================
#URUNLERI SILME 
#=======================================================

@router.delete("/{product_id}")
def delete_product(product_id: int, db: Session= Depends(get_db), current_user: int= Depends(auth.get_current_user)):
    db_product = db.query(model.Product).filter(model.Product.id == product_id).first()
    
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    db.query(model.CartItem).filter(
    model.CartItem.product_id == product_id
            ).delete()
    db.delete(db_product)

    db.commit()
    return {"message": "Product has been succesfully delete"}
