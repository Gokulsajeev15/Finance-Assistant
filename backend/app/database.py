import os
import logging
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, select
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Connection
# ---------------------------------------------------------------------------
# asyncpg+postgresql tells SQLAlchemy to use the asyncpg driver (async).
# Without async, every DB query would freeze the server until it finished —
# same problem we discussed with requests vs httpx.
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+asyncpg://gokulsajeev@localhost/finance_assistant"
)

# The engine is the connection pool — a set of open connections to the DB
# that FastAPI reuses across requests instead of opening a new one each time.
engine = create_async_engine(DATABASE_URL, echo=False)

# A session is one "unit of work" with the DB — like a shopping cart.
# You add operations to it, then commit them all at once.
# async_sessionmaker gives us a factory to create sessions on demand.
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)


# ---------------------------------------------------------------------------
# Table definition
# ---------------------------------------------------------------------------
# DeclarativeBase is the parent class for all our table models.
# SQLAlchemy looks at these classes to know what tables to create.
class Base(DeclarativeBase):
    pass


class Message(Base):
    """One row = one message in the conversation."""
    __tablename__ = "conversations"

    id         = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(String(100), nullable=False, index=True)  # groups messages by conversation
    role       = Column(String(10), nullable=False)               # "user" or "ai"
    content    = Column(Text, nullable=False)                     # what was said
    created_at = Column(DateTime, default=lambda: datetime.utcnow())


# ---------------------------------------------------------------------------
# Startup
# ---------------------------------------------------------------------------
async def init_db():
    """Create the conversations table if it doesn't exist yet.
    Called once when the FastAPI app starts up."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("Database ready")


# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------
async def save_message(session_id: str, role: str, content: str):
    """Save one message (user or AI) to the database."""
    async with AsyncSessionLocal() as session:
        message = Message(session_id=session_id, role=role, content=content)
        session.add(message)
        await session.commit()


async def get_history(session_id: str, limit: int = 10) -> list[dict]:
    """Fetch the last N messages for a session, oldest first.

    We cap at 10 messages because LLMs have a token limit —
    sending the entire history of a long conversation would
    eventually exceed it and cause errors.
    """
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(Message)
            .where(Message.session_id == session_id)
            .order_by(Message.created_at.desc())  # newest first so LIMIT cuts old messages
            .limit(limit)
        )
        messages = result.scalars().all()
        # Reverse so the LLM reads them oldest → newest (natural order)
        return [{"role": m.role, "content": m.content} for m in reversed(messages)]
