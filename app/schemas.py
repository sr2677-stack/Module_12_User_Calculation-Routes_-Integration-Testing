from datetime import datetime
from pydantic import BaseModel, EmailStr
from typing import Literal

# ── User schemas ──────────────────────────────────────────────
class UserCreate(BaseModel):
    email:    EmailStr
    username: str
    password: str

class UserRead(BaseModel):
    id:         int
    email:      EmailStr
    username:   str
    created_at: datetime

    model_config = {"from_attributes": True}

class UserLogin(BaseModel):
    email:    EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type:   str = "bearer"

# ── Calculation schemas ───────────────────────────────────────
OperationType = Literal["add", "subtract", "multiply", "divide"]

class CalculationCreate(BaseModel):
    operation: OperationType
    operand_a: float
    operand_b: float

class CalculationUpdate(BaseModel):
    operation: OperationType | None = None
    operand_a: float | None = None
    operand_b: float | None = None

class CalculationRead(BaseModel):
    id:         int
    operation:  str
    operand_a:  float
    operand_b:  float
    result:     float
    created_at: datetime
    user_id:    int

    model_config = {"from_attributes": True}