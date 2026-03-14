from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import or_
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import Model as model
import Schemas as schemas
from database import get_db
import hashlib
import traceback
from config import settings


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")
 
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
 
    normalized = hashlib.sha256(password.encode("utf-8")).hexdigest()
   
    return pwd_context.hash(normalized)

def verify_password(plain_password, hashed_password):
    normalized = hashlib.sha256(plain_password.encode("utf-8")).hexdigest()
    return pwd_context.verify(normalized, hashed_password)

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt

def get_current_user(token: str= Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Couldn't validate credentials",
        headers={"WWW-Authenticate": "Bearer"},

    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except:
        raise credentials_exception
    

    user = db.query(model.User).filter(
        model.User.id == user_id
    ).first()

    if user is None:
        raise credentials_exception
    return user


#================================================================
#REGISTER
#===============================================================
@router.post("/register", response_model=schemas.RegisterResponse)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    try:
        existing_user = db.query(model.User).filter(
            or_(
                model.User.email == user.email,
                model.User.username == user.username
            )
        ).first()

        if existing_user:
            return {
                "success": False,
                "message": "This username or email is already registered.",
                "data": None
            }

        hashed_password = get_password_hash(user.password)

        new_user = model.User(
            username=user.username,
            email=user.email,
            hashed_password=hashed_password
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return {
            "success": True,
            "message": "Registration successfully created",
            "data": {
                "id": new_user.id,
                "username": new_user.username,
                "email": new_user.email,
                "is_staff": False
            }
        }

    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


#==============================================================
#         LOGIN
#==============================================================
@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = db.query(model.User).filter(
        model.User.username == form_data.username
    ).first()

    if not user or not verify_password(
        form_data.password,
        user.hashed_password
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Username or password incorrect",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(
        data={"sub": str(user.id)}
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }



def admin_required(current_user = Depends(get_current_user)):
    if not current_user.is_staff:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin Only")
    return current_user



