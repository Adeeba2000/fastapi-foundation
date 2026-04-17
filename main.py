from typing import Annotated, Union

from fastapi import FastAPI, Path, HTTPException, Query, Depends
import models
from schemas import User, UserResponse, UserUpdate
from sqlalchemy.orm import Session

#from data.users import users
from database import Base, engine, get_db

app = FastAPI()

Base.metadata.create_all(bind=engine)

@app.post("/users", response_model = UserResponse)
def create_user(user: User, db: Annotated[Session, Depends(get_db)]):
    new_user = models.User(**user.model_dump())

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@app.get("/users", response_model = list[UserResponse])
def get_users(db: Annotated[Session, Depends(get_db)]):
    users = db.query(models.User).all()  #select * from users
    return users

# Path Params
@app.get("/users/{user_id}", response_model = UserResponse)
def get_user(user_id: int, db: Annotated[Session, Depends(get_db)]):
    user = db.query(models.User).filter(models.User.id == user_id).first() # select * from users where id = user_id
    # first() returns first matching record or None

    if not user:
        raise HTTPException(status_code=404, detail = 'User not found')
    
    return user

@app.get("/users/city/delhi", response_model = UserResponse)
def get_delhi_users(db: Annotated[Session, Depends(get_db)]):
    delhi_users = db.query(models.User).filter(models.User.city == 'Delhi').all()

    if not delhi_users:
        raise HTTPException(status_code=404, detail = 'Delhi user not found')
    
    return delhi_users


@app.patch("/users/{user_id}", response_model= UserResponse)
def update_user(user_id: int, user: UserUpdate, db: Annotated[Session, Depends(get_db)]):

    db_user = db.query(models.User).filter(models.User.id == user_id).first()

    if not db_user:
        raise HTTPException(status_code= 404, detail='User not found')
    
    update_data = user.model_dump(exclude_unset=True)    # only update provided fields None fields stay as it is

    for key, value in update_data.items():
        setattr(db_user, key, value)

    db.commit()
    db.refresh(db_user)

    return db_user

@app.delete("/users/{user_id}")
def delete_user(user_id: int, db: Annotated[Session, Depends(get_db)]):

    user_to_delete = db.query(models.User).filter(models.User.id == user_id).first()

    if not user_to_delete:
        raise HTTPException(status_code= 404, detail='User not found')
    
    db.delete(user_to_delete)
    db.commit()

    return {"message": "User deleted successfully"}

# # Path Params
# @app.get("/users/{id}")
# def get_specific_user(id: int = Path(..., description= 'ID of the user in the DB', examples = 1)):
#     for user in users:
#         if user["id"] == id:
#             return user
    
#     raise HTTPException(status_code=404, detail="User not found")

# # Query Params
# @app.get("/sort")
# def sort_users(sort_by :Union[int, str]= Query(..., description = 'Sort on the basis of id, name'), order: str= Query('asc', description= 'Sort in asc or desc order.')):
#     if sort_by not in ['id', 'name']:
#         raise HTTPException(status_code=400, detail = 'Invalid selection of value.')
    
#     if order not in ['asc','desc']:
#         raise HTTPException(status_code= 404, detail = 'Invalid order select.')
    
#     sort_order = True if order == 'desc' else False
#     sorted_data = sorted(users, key=lambda user: user[sort_by], reverse = sort_order)
    
#     return sorted_data
