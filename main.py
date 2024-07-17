import os
import re
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException, Depends
import asyncpg
import bcrypt
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()

async def db_connect():
    connection = await asyncpg.connect(
        user=os.getenv("POSTGRES_USER"), password=os.getenv("POSTGRES_PASSWORD"),
        database=os.getenv("POSTGRES_DB"), host=os.getenv("POSTGRES_HOST"))
    try:
        yield connection
    finally:
        await connection.close()

class UserBody(BaseModel):
    name: str
    email: str
    password: str

@app.get("/")
async def healthcheck():
    return {"message": "I'm healthy'"}

@app.post("/create")
async def create_user(user: UserBody, db: asyncpg.Connection = Depends(db_connect)):
    if len(user.password) < 8:
        raise HTTPException(status_code=500, detail="Password must bee longer than 8 chars")

    if not re.match(r'^[\w\.-]+@[a-zA-Z\d\.-]+\.[a-zA-Z]{2,}$', user.email):
        raise HTTPException(status_code=500, detail="Email is not valid")

    try:
        hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())
        query = "INSERT INTO users (name, email, password) VALUES ($1, $2, $3)"
        await db.execute(query, user.name, user.email, hashed_password.decode('utf-8'))
        return {"message": "User created successfully"}
    except asyncpg.exceptions.UniqueViolationError:
        raise HTTPException(status_code=400, detail="Another user has this email")
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

def check_password(password, hash_password):
    return bcrypt.checkpw(password.encode('utf-8'), hash_password.encode('utf-8'))

class UpdateNameBody(BaseModel):
    email: str
    name: str
    password: str

@app.put("/updatename")
async def update_name(body: UpdateNameBody, db: asyncpg.Connection = Depends(db_connect)):
    try:
        query = "SELECT password FROM users WHERE email = $1"
        result = await db.fetch(query, body.email)
        
        hash_password = result[0]['password']
        
        if not check_password(body.password, hash_password):
            raise HTTPException(status_code=500, detail="incorrect password")

        query = "UPDATE users SET name=$1 WHERE email=$2"
        result = await db.execute(query, body.name, body.email)
        return {"message": "User updated successfully"}
    except IndexError:
        raise HTTPException(status_code=404, detail=str("User Not Found"))

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/delete/{id}")
async def delete_users(id: int, db: asyncpg.Connection = Depends(db_connect)):
    try:
        query = "DELETE FROM users WHERE id=$1"
        result = await db.execute(query, id)
        if result == 'DELETE 0':
            raise HTTPException(status_code=404, detail=str("User Not Found"))

        return {"message": "User deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

