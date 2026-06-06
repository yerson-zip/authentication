from sqlalchemy import  Column, Integer, String, Boolean, TIMESTAMP, ForeignKey, text
from app.core.database import Base

class RefreshToken(Base):
    __tablename__ = "refresh_tokens"

    id = Column(Integer, primary_key=True, autoincrement=True)
    token = Column(String, nullable=False, unique=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    expires_at= Column(TIMESTAMP(timezone=True), nullable=False)
    revoked = Column(Boolean, nullable=False, server_default=text("false"))
    creat_at= Column(TIMESTAMP(timezone=True), server_default=text("now()"))
