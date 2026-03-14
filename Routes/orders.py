from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session 
from typing import List 
import Model as model
import Schemas as schemas
from database import get_db
from routers import auth
from routers.auth import admin_required

router = APIRouter(
    prefix="/orders",
    tags=["Orders"]
)

#===============================
# pass order list
#===============================

@router.get("/", response_model=List[schemas.Order])
def read_orders(db: Session = Depends(get_db), current_user: int = Depends(auth.get_current_user)):
    
    orders = db.query(model.Order).filter(
        model.Order.user_id == current_user.id
    ).all()
    return orders

@router.post("/", response_model=schemas.Order)
def create_order(db: Session= Depends(get_db), current_user: int = Depends(auth.get_current_user)):
    cart = db.query(model.Cart).filter(
        model.Cart.user_id == current_user.id
    ).first()

    if not cart or not cart.items:
        raise HTTPException(status_code=400, detail="Your cart is empty, no orders can be placed")

    new_order = model.Order(
        user_id = current_user.id,
        status="Processing"
    )
    db.add(new_order)
    db.commit()
    db.refresh(new_order)
    
    total_price = 0
    for cart_item in cart.items:
        order_item= model.OrderItem(
            order_id = new_order.id, 
            product_id = cart_item.product_id,
            quantity = cart_item.quantity,
            price = cart_item.product.price
        )
        total_price += cart_item.quantity * cart_item.product.price
        db.add(order_item)

    new_order.total_price = total_price

    db.query(model.CartItem).filter(
        model.CartItem.cart_id == cart.id
    ).delete()

    db.commit()
    db.refresh(new_order)

    return new_order



@router.get("/admin/orders")
def get_all_orders(
    db: Session = Depends(get_db),
    current_user = Depends(admin_required)
):
   return db.query(model.Order).all()



  