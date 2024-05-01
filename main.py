from typing import List, Optional
import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import date

app = FastAPI()


class User(BaseModel):
    id: int
    username: str
    wallet: float
    birthdate: date


db_users = [
    User(id=1, username="David", wallet=10.0, birthdate=date(1990, 1, 1)),
    User(id=2, username="Eric", wallet=200.0, birthdate=date(1982, 5, 15)),
    User(id=3, username="Gera", wallet=500.0, birthdate=date(1995, 6, 12)),
    User(id=4, username="Kurt", wallet=2000.0, birthdate=date(1975, 2, 17)),
    User(id=5, username="Simon", wallet=30000.0, birthdate=date(1989, 12, 22)),
]


@app.get("/users", response_model=List[User], tags=["Users"])
async def get_users(limit: int = 10, offset: int = 0) -> List[User]:
    if len(db_users) == 0:
        raise HTTPException(status_code=404, detail="Список пользователей пуст")
    return db_users[offset:][:limit]


@app.get("/users/{user_id}", response_model=User, tags=["Users"])
async def get_user(user_id: int) -> User:
    user = next((user for user in db_users if user.id == user_id), None)
    if user is None:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    return user


@app.post(path="/users", response_model=User, tags=["Users"])
async def create_user(user: User) -> User:
    db_users.append(user)
    return user


@app.delete(path="/users/{user_id}", tags=["Users"])
async def delete_user(user_id: int):
    user = next((user for user in db_users if user.id == user_id), None)
    if user is None:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    index = db_users.index(user)
    db_users.pop(index)
    return {"message": "Пользователь удален."}


@app.put(path="/users/{user_id}", response_model=User, tags=["Users"])
async def update_book(user_id: int, user: User) -> User:
    user_put = next((user for user in db_users if user.id == user_id), None)
    if user_put is None:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    index = db_users.index(user_put)
    db_users[index] = user
    return db_users[index]

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
