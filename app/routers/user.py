from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import asc, desc, select
from sqlalchemy.orm import Session
from typing import Annotated, List, Union
from app.schemas import User, UserResponse, UserUpdate

import app.models as models
from app.database import get_db

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.get("/", response_model=List[UserResponse])
def get_users(db: Annotated[Session, Depends(get_db)]):
    result = db.execute(select(models.User))
    users = result.scalars().all()
    return users

@router.post("/", response_model = UserResponse)
def create_user(user: User, db: Annotated[Session, Depends(get_db)]):
    new_user = models.User(**user.model_dump())

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@router.get("/{user_id}", response_model = UserResponse)
def get_user(user_id: int, db: Annotated[Session, Depends(get_db)]):
    result = db.execute(select(models.User).where(models.User.id == user_id))  #user = db.query(models.User).filter(models.User.id == user_id).first() # select * from users where id = user_id
    user = result.scalars().first()  # first() returns first matching record or None

    if not user:
        raise HTTPException(status_code=404, detail = 'User not found')
    
    return user

@router.get("/city/delhi", response_model = UserResponse)
def get_delhi_users(db: Annotated[Session, Depends(get_db)]):
    result = db.execute(select(models.User).where(models.User.city == 'Delhi'))
    delhi_users = result.scalars().all()

    if not delhi_users:
        raise HTTPException(status_code=404, detail = 'Delhi user not found')
    
    return delhi_users


@router.patch("/{user_id}", response_model= UserResponse)
def update_user(user_id: int, user: UserUpdate, db: Annotated[Session, Depends(get_db)]):

    result = db.execute((models.User).where(models.User.id == user_id))
    db_user = result.scalars().first()

    if not db_user:
        raise HTTPException(status_code= 404, detail='User not found')
    
    update_data = user.model_dump(exclude_unset=True)    # only update provided fields None fields stay as it is

    for key, value in update_data.items():
        setattr(db_user, key, value)

    db.commit()
    db.refresh(db_user)

    return db_user

@router.delete("/{user_id}")
def delete_user(user_id: int, db: Annotated[Session, Depends(get_db)]):

    result = db.execute((models.User).where(models.User.id == user_id))
    user_to_delete = result.scalars().first()

    if not user_to_delete:
        raise HTTPException(status_code= 404, detail='User not found')
    
    db.delete(user_to_delete)
    db.commit()

    return {"message": "User deleted successfully"}
