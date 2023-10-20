from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Identity,
    Integer,
    LargeBinary,
    MetaData,
    String,
    Table,
    func,
)
from sqlalchemy.dialects.postgresql import UUID

from src.constants import DB_NAMING_CONVENTION

metadata = MetaData(naming_convention=DB_NAMING_CONVENTION)


auth_user = Table(
    "auth_user",
    metadata,
    Column("id", Integer, Identity(), primary_key=True),
    Column("login_id", String, nullable=False, unique=True),
    Column("login_password", LargeBinary, nullable=False),
    Column("user_name", String),
    Column("nick_name", String, unique=True),
    Column("image_url", String),
    Column("is_admin", Boolean, server_default="false", nullable=False),
    Column("created_at", DateTime, server_default=func.now(), nullable=False),
    Column("updated_at", DateTime, onupdate=func.now()),
)


auth_refresh_token = Table(
    "auth_refresh_token",
    metadata,
    Column("uuid", UUID, primary_key=True),
    Column("user_id", ForeignKey("auth_user.id", ondelete="CASCADE"), nullable=False),
    Column("refresh_token", String, nullable=False),
    Column("expires_at", DateTime, nullable=False),
    Column("created_at", DateTime, server_default=func.now(), nullable=False),
    Column("updated_at", DateTime, onupdate=func.now()),
)
