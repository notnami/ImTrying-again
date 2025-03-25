from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Boolean, ForeignKey


DATABASE_URL = "sqlite:///./social_media.db"

# Setup the SQLite engine and metadata
engine = create_engine(DATABASE_URL)
metadata = MetaData()

# Define Users table
users = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("username", String, unique=True, index=True),
    Column("image_url", String),
    Column("is_admin", Boolean, default=False)
)

# Define Posts table
posts = Table(
    "posts",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("title", String),
    Column("post_text", String),
    Column("user_id", Integer, ForeignKey("users.id")),
    Column("likes", Integer, default=0)
)

# Create the tables in the database
metadata.create_all(engine)
