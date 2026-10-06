import os
from dotenv import load_dotenv

load_dotenv()

groq_api = os.getenv("GROQ_API_KEY")
notion_api = os.getenv("NOTION_API_KEY")
notion_db_id = os.getenv("NOTION_DB_ID") or os.getenv("NOTION_DATABASE_ID")

if not groq_api:
    raise ValueError("GROQ_API_KEY not found in environment variables")

if not notion_api:
    raise ValueError("NOTION_API_KEY not found in environment variables")

if not notion_db_id:
    raise ValueError("NOTION_DB_ID (or NOTION_DATABASE_ID) not found in environment variables")