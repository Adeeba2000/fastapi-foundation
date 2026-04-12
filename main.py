from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

users = [
    {"id": 1, "name": "Aman", "email": "aman@example.com"},
    {"id": 2, "name": "Sara", "email": "sara@example.com"},
    {"id": 3, "name": "Rahul", "email": "rahul@example.com"}
]

@app.get("/", response_class= HTMLResponse)
def home():
    return f"<h1>{users[0]['name']}</h1>"

@app.get("/api/users")
def get_user():
    return users