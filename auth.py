from fastapi import APIRouter, HTTPException, Depends
from databases import Database
from sqlalchemy import select
from models import users  # Make sure users model is defined correctly

DATABASE_URL = "sqlite:///./social_media.db"  
database = Database(DATABASE_URL)


router = APIRouter()

# Dependency to get the database connection
async def get_database() -> Database:
    database = Database(DATABASE_URL)
    await database.connect()
    try:
        yield database
    finally:
        await database.disconnect()

@router.post("/login")
async def login(username: str, db: Database = Depends(get_database)):
    # Create a SQLAlchemy query
    query = select(users).where(users.c.username == username)
    user = await db.fetch_one(query)

    if user:
        return {"message": f"Welcome back, {username}!", "is_admin": user["is_admin"]}  
    else:
        raise HTTPException(status_code=400, detail="User not found")

# Logout
@router.post("/logout")
def logout():
    return {"success": True}
