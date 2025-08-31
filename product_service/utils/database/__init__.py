import asyncio
import asyncpg


async def is_postgres_healthy(
    host: str,
    port: int,
    user: str,
    password: str,
    database: str,
    retries: int = 5,
    delay: int = 2,
) -> bool:
    for attempt in range(1, retries + 1):
        try:
            conn = await asyncpg.connect(
                host=host,
                port=port,
                user=user,
                password=password,
                database=database,
                timeout=3,
            )
            await conn.close()
            print(f"[✓] PostgreSQL is available (attempt {attempt})")
            return True
        except (asyncpg.PostgresError, OSError) as e:
            print(f"[!] Connection error (attempt {attempt}): {e}")
            await asyncio.sleep(delay)

    print("[✗] PostgreSQL is not available after all attempts")
    return False