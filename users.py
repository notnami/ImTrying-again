from fastapi import APIRouter, HTTPException, Depends
from databases import Database
from sqlalchemy import select, insert, delete
from models import users  # Ensure the users model is updated accordingly

DATABASE_URL = "sqlite:///./social_media.db"
database = Database(DATABASE_URL)

router = APIRouter()

# Dependency to get the database connection
async def get_database() -> Database:
    if not database.is_connected:
        await database.connect()
    return database

@router.get("/{id}")
async def get_user(id: int, db: Database = Depends(get_database)):
    query = users.select().where(users.c.id == id)
    user = await db.fetch_one(query)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.post("/")
async def create_user(username: str, image_url: str, is_admin: bool, db: Database = Depends(get_database)):
    query = users.insert().values(username=username, image_url=image_url, is_admin=is_admin)  # Updated field name
    last_record_id = await db.execute(query)
    return {"id": last_record_id, "username": username, "image_url": image_url, "is_admin": is_admin}  # Updated field name

@router.delete("/{id}")
async def delete_user(id: int, db: Database = Depends(get_database)):
    query = users.delete().where(users.c.id == id)
    await db.execute(query)
    return {"success": True}
