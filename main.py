from typing import Union

from fastapi import FastAPI, Path, HTTPException, Query
from fastapi.responses import HTMLResponse

from data.users import users

app = FastAPI()

@app.get("/", response_class= HTMLResponse)
def home():
    return f"<h1>{users[0]['name']}</h1>"

@app.get("/api/users")
def get_users():
    return users

# Path Params
@app.get("/users/{id}")
def get_specific_user(id: int = Path(..., description= 'ID of the user in the DB', examples = 1)):
    for user in users:
        if user["id"] == id:
            return user
    
    raise HTTPException(status_code=404, detail="User not found")

# Query Params
@app.get("/sort")
def sort_users(sort_by :Union[int, str]= Query(..., description = 'Sort on the basis of id, name'), order: str= Query('asc', description= 'Sort in asc or desc order.')):
    if sort_by not in ['id', 'name']:
        raise HTTPException(status_code=400, detail = 'Invalid selection of value.')
    
    if order not in ['asc','desc']:
        raise HTTPException(status_code= 404, detail = 'Invalid order select.')
    
    sort_order = True if order == 'desc' else False
    sorted_data = sorted(users, key=lambda user: user[sort_by], reverse = sort_order)
    
    return sorted_data
