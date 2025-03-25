from fastapi import APIRouter, HTTPException, Depends
from databases import Database
from sqlalchemy import select, insert, delete
from models import posts

DATABASE_URL = "sqlite:///./social_media.db"  # Adjust as necessary
database = Database(DATABASE_URL)

router = APIRouter()

# Dependency to get the database connection
async def get_database() -> Database:
    if not database.is_connected:
        await database.connect()
    return database

@router.post("/")
async def create_post(title: str, post_text: str, user_id: int, db: Database = Depends(get_database)):
    query = posts.insert().values(title=title, post_text=post_text, user_id=user_id)
    last_record_id = await db.execute(query)
    return {"id": last_record_id, "title": title, "post_text": post_text, "user_id": user_id}

@router.get("/{postId}")
async def get_post(postId: int, db: Database = Depends(get_database)):
    query = posts.select().where(posts.c.id == postId)
    post = await db.fetch_one(query)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post

@router.delete("/{postId}")
async def delete_post(postId: int, db: Database = Depends(get_database)):
    query = posts.delete().where(posts.c.id == postId)
    await db.execute(query)
    return {"success": True}
