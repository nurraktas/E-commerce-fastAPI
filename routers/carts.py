from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import Model as model
import Schemas as schemas
from database import get_db
from exceptions import CartNotFoundException, OutOfStockException
from routers import auth

router=APIRouter (
    prefix="/carts",
    tags=["Carts"]
)

@router.get("/my-cart", response_model=schemas.Cart)
def read_user_cart(db: Session = Depends(get_db), current_user: model.User = Depends(auth.get_current_user)):
    db_cart = db.query(model.Cart).filter(
        model.Cart.user_id == current_user.id
    ).first()

    if not db_cart:
        raise HTTPException(
            status_code= 404, 
            detail="You don't have a basket"
        )
    return db_cart

#==========================================================
# CART LISTELEME
#==========================================================
@router.get("/{cart_id}", response_model=schemas.CartResponse)
def read_cart(cart_id: int, db:Session =Depends(get_db), current_user: int = Depends(auth.get_current_user)):
    db_cart = db.query(model.Cart).filter(
        model.Cart.id == cart_id,
        model.Cart.user_id == current_user.id
        ).first()
    if not db_cart:
      raise  CartNotFoundException()  

    return db_cart  

#=========================================================
#SEPET EKLEME
#=========================================================
@router.post("/", response_model=schemas.Cart)
def create_cart(db: Session = Depends(get_db), current_user: model.User = Depends(auth.get_current_user)):
    
    existing_cart = db.query(model.Cart).filter(
        model.Cart.user_id == current_user.id
    ).first()

    if existing_cart:
        return existing_cart

    db_cart = model.Cart(user_id = current_user.id)
    db.add(db_cart)
    db.commit()
    db.refresh(db_cart)
    return db_cart


#===========================================================
#!!!  SEPETE URUN EKLEME  !!!!!!!!
#=============================================================

@router.post("/items/", response_model=schemas.Cart)
def add_item_to_cart(cart_id: int, item: schemas.CartItemCreate, db: Session = Depends(get_db), current_user: int= Depends(auth.get_current_user)):
    
    try:
        print(f"--- İŞLEM BAŞLIYOR: Sepet ID: {cart_id}, Ürün ID: {item.product_id} ---")

        # 1. Sepet Kontrolü
        db_cart = db.query(model.Cart).filter(
            model.Cart.user_id == current_user.id
        ).first()
        if not db_cart:
            print("HATA: Sepet veritabanında bulunamadı!")
            raise HTTPException(status_code=404, detail="This product doesn't find")
        
        # 2. Ürün Kontrolü
        db_product = db.query(model.Product).filter(model.Product.id == item.product_id).first()
        if not db_product:
            print("HATA: Ürün veritabanında bulunamadı!")
            raise HTTPException(status_code=404, detail="This product doesn't find")
        
        # 3. Ara Tabloya Ekleme
        print("--- Kayıt hazırlanıyor... ---")
        existing_item = db.query(model.CartItem).filter(
             model.Cart.user_id == current_user.id,
             model.CartItem.product_id == item.product_id
             ).first()

        if existing_item:
            total_wanted = existing_item.quantity + item.quantity
        else:
            total_wanted = item.quantity
        
        if db_product.stock < total_wanted:
            raise OutOfStockException()
        

        if existing_item:
            existing_item.quantity += item.quantity
        else:
            db_item = model.CartItem(
                cart_id = cart_id,
                product_id= item.product_id,
                quantity= item.quantity
            )
            db.add(db_item)
        db.commit()
        db.refresh(db_cart)


        return db_cart
    
    except OutOfStockException:
        raise HTTPException(status_code=400, detail="Üzgünüz, stok yetersiz! Sepete bu kadar ürün ekleyemezsiniz.")

    except HTTPException as http_ex:
        # 404 gibi standart hataları olduğu gibi fırlat
        raise http_ex

    except Exception as e:
        # Beklenmeyen diğer tüm hatalar (kod hatası vb.)
        hata_detayi = traceback.format_exc()
        print("!!! KRİTİK HATA !!!", hata_detayi)
        raise HTTPException(status_code=500, detail=f"Sunucu Hatası: {str(e)}")


#SATIN ALMA ISLEMI 
#=========================================================
@router.post("/checkout")
def checkout(
    cart_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(auth.get_current_user)
):
    cart = db.query(model.Cart).filter(
        model.Cart.id == cart_id,
        model.Cart.user_id == current_user.id
    ).first()

    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")

    if not cart.items:
        raise HTTPException(status_code=400, detail="Cart is empty")

    total_price = 0

    
    order = model.Order(
        user_id=current_user.id,
        status="Processing"
    )
    db.add(order)
    db.commit()
    db.refresh(order)

   
    for item in cart.items:
        product = item.product

        if product.stock < item.quantity:
            raise HTTPException(
                status_code=400,
                detail=f"Not enough stock for {product.name}"
            )

        product.stock -= item.quantity

        order_item = model.OrderItem(
            order_id=order.id,
            product_id=product.id,
            quantity=item.quantity,
            price=product.price
        )

        db.add(order_item)
        total_price += product.price * item.quantity


    for item in cart.items:
        db.delete(item)

    order.total_price = total_price

    db.commit()
    db.refresh(order)

    return order


#============================================================
#SEPETE KONULAN URUNU GUNCELLEME
#============================================================
@router.put("/items/{product_id}")
def uptade_cart_item(cart_id: int, product_id: int,item_data: schemas.CartItemUpdate, db: Session = Depends(get_db), current_user: int= Depends(auth.get_current_user)):
    print(f"The cart will have {cart_id}, and the number of products will be {product_id}")
      
    db_item= db.query(model.CartItem).filter(
        model.Cart.user_id == current_user.id,
        model.CartItem.product_id == product_id
    ).first()

    if not db_item:
        raise HTTPException(status_code=404, detail="Cart not found")

    db_item.quantity = item_data.quantity
    db.commit()
    db.refresh(db_item)

    return {"message": "Quantity uptated", "new_quantity":db_item.quantity}




#====================================================
# SEPETTEN URUN CIKARMA
#=====================================================

@router.delete("/items/{product_id}")
def delete_item_from_cart(cart_id: int, product_id: int, db: Session = Depends(get_db), current_user: int= Depends(auth.get_current_user)):
        print(f"Product {product_id} is being deleted from the cart {cart_id}.")

        db_item = db.query(model.CartItem).filter(
             model.Cart.user_id == current_user.id,
            model.CartItem.product_id == product_id
        ).first()

        if not db_item:
            raise HTTPException(status_code=404, detail="This product is not in your cart.")
        
        db.delete(db_item)
        db.commit()
        return {"message": "The product has been successfully removed from the cart"}


