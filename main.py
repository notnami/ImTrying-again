from fastapi import FastAPI
from users import router as users_router
from auth import router as auth_router  # Make sure this is included
from posts import router as posts_router  # Make sure this is included
from databases import Database


DATABASE_URL = "sqlite:///./social_media.db"
database = Database(DATABASE_URL)


from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Add CORS middleware to allow requests from the Blazor frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5000"],  # Specify the Blazor frontend's URL
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Allow all headers
)


# Register the routers
app.include_router(auth_router, prefix="/api/auth")
app.include_router(users_router, prefix="/api/users")
app.include_router(posts_router, prefix="/api/posts")

# Connect/disconnect to the database on app startup/shutdown
@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

@app.get("/")
def read_root():
    return {"message": "Welcome to ShinraNet!"}
