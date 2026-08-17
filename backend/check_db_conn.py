import asyncio
from dotenv import load_dotenv
import os
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text
from pathlib import Path
import socket
from urllib.parse import urlparse

# Determine root folder (one directory up from 'backend')
BASE_DIR = Path(__file__).resolve().parent.parent
env_path = BASE_DIR / ".env"

# Load the .env file explicitly
load_dotenv(dotenv_path=env_path)

async def test_connection():
    raw_url = os.getenv("SUPABASE_DB_URL")
    if not raw_url:
        print(f"❌ Error: SUPABASE_DB_URL is not set in {env_path}")
        return
    
    # Sanitize & check URL components
    # Handle postgresql+asyncpg:// schema parsing
    parse_url = raw_url.replace("postgresql+asyncpg://", "http://")
    parsed = urlparse(parse_url)

    print("🔍 Connection String Diagnostic:")
    print(f"  - Scheme check: {'OK' if raw_url.startswith('postgresql+asyncpg://') else '❌ Must start with postgresql+asyncpg://'}")
    print(f"  - Hostname extracted: {parsed.hostname}")
    print(f"  - Port: {parsed.port or 5432}")
    print(f"  - Database Name: {parsed.path.lstrip('/')}")

    if not parsed.hostname:
        print("❌ Error: Hostname could not be parsed from SUPABASE_DB_URL")
        return
    
    # Try DNS resolution on hostname
    print(f"\n⏳ Testing DNS resolution for host '{parsed.hostname}'...")
    try:
        ip = socket.gethostbyname(parsed.hostname)
        print(f"✅ DNS Resolved successfully! IP: {ip}")
    except socket.gaierror as e:
        print(f"❌ DNS Resolution Failed: {e}")
        print("\n💡 Troubleshooting Tips:")
        print("1. Did you copy host from Supabase? Example: db.xxx.supabase.co or aws-0-us-east-1.pooler.supabase.com")
        print("2. Check for extra characters, quotes, spaces, or leading 'https://' in your host.")
        print("3. Check if Supabase Project status is Active in Supabase dashboard.")
        return

    # Attempt actual DB Connection
    print("\n⏳ Attempting Async Database Connection...")
    try:
        engine = create_async_engine(raw_url, echo=False)
        async with engine.connect() as conn:
            result = await conn.execute(text("SELECT version();"))
            row = result.scalar()
            print("✅ Connection successful!")
            print(f"📊 PostgreSQL Version: {row}")
        await engine.dispose()
    except Exception as e:
        print("❌ Connection failed!")
        print(f"Error details: {e}")


if __name__ == "__main__":
    asyncio.run(test_connection())