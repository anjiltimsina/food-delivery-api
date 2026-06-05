from sqlalchemy.ext.asyncio import AsyncSession , create_async_engine , async_sessionmaker
from app.core.config import settings 

#Connection Pooling is a technique where a fixed set of database connections is created and reused by multiple requests instead of creating and destroying a new connection for every database operation, improving performance and reducing database overhead.

#A database connection is just: A live communication link between your Python app and PostgreSQL.
engine = create_async_engine(
    settings.DATABASE_URL,
    echo = settings.DEBUG, # echo true bhane sql queries haru console ma print huncha
    pool_size =10, # pool_size le connection pool ma kati connections rakhne ho bhanne ho
    max_overflow =20, # max_overflow le pool_size bhanda badhi kati connections create garna milcha bhanne ho
)
# so 30 connections samma use garnu milyo



#expire_on_commit -->Keep data in memory after commit --Do NOT re-query database
AsyncSessionLocal = async_sessionmaker(
    bind = engine ,
    class_ = AsyncSession,
    expire_on_commit = False, # expire_on_commit false bhane session commit garepaxi pani objects haru valid rahanchan
)

async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session # give session to route
            await session.commit() # Save all changes to database permanently
        except Exception as e:
            await session.rollback() 
            raise

"""
rollback()

Means:

Undo everything done in this request
"""