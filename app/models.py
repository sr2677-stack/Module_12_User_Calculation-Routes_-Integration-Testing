from datetime import datetime
from sqlalchemy import String, Float, ForeignKey, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id:         Mapped[int]      = mapped_column(primary_key=True, index=True)
    email:      Mapped[str]      = mapped_column(String(255), unique=True, index=True)
    username:   Mapped[str]      = mapped_column(String(100), unique=True, index=True)
    hashed_pw:  Mapped[str]      = mapped_column(String(255))
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    calculations: Mapped[list["Calculation"]] = relationship(back_populates="owner")


class Calculation(Base):
    __tablename__ = "calculations"

    id:          Mapped[int]      = mapped_column(primary_key=True, index=True)
    operation:   Mapped[str]      = mapped_column(String(50))   # e.g. "add", "multiply"
    operand_a:   Mapped[float]    = mapped_column(Float)
    operand_b:   Mapped[float]    = mapped_column(Float)
    result:      Mapped[float]    = mapped_column(Float)
    created_at:  Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    user_id:     Mapped[int]      = mapped_column(ForeignKey("users.id"))

    owner: Mapped["User"] = relationship(back_populates="calculations")