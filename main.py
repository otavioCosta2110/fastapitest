import re
from typing import Union
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException, Depends
import asyncpg

app = FastAPI()

async def db_connect():
    connection = await asyncpg.connect(
        user='user', password='senha123',
        database='database', host='db')
    try:
        yield connection
    finally:
        await connection.close()

class UserBody(BaseModel):
    name: str
    email: str
    password: str

@app.post("/create")
async def create_user(user: UserBody, db: asyncpg.Connection = Depends(db_connect)):
    if len(user.password) < 8:
        raise HTTPException(status_code=500, detail="Password must bee longer than 8 chars")

    if not re.match(r'^[\w\.-]+@[a-zA-Z\d\.-]+\.[a-zA-Z]{2,}$', user.email):
        raise HTTPException(status_code=500, detail="Email is not valid")

    try:
        query = "INSERT INTO users (name, email, password) VALUES ($1, $2, $3)"
        await db.execute(query, user.name, user.email, user.password)
        return {"message": "User created successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/list")
async def list_users(db: asyncpg.Connection = Depends(db_connect)):
    try:
        query = "SELECT id, name, email FROM users"
        users = await db.fetch(query)
        return users
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

class UpdateNameBody(BaseModel):
    email: str
    name: str
    password: str

@app.put("/updatename")
async def update_name(body: UpdateNameBody, db: asyncpg.Connection = Depends(db_connect)):
    try:
        query = "UPDATE users SET name=$1 WHERE email=$2 AND password=$3"
        await db.execute(query, body.name, body.email, body.password)
        return {"message": "User updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/delete/{id}")
async def delete_users(id: int, db: asyncpg.Connection = Depends(db_connect)):
    try:
        query = "DELETE FROM users WHERE id=$1"
        await db.execute(query, id)
        return {"message": "User deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

