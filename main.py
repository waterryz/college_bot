from db import init_db
from bot import main
import asyncio

if __name__ == "__main__":
    init_db()
    asyncio.run(main())
