from passlib.context import CryptContext

# bcrypt + passlib is fragile on newer Python/bcrypt combos.
# pbkdf2_sha256 is stable and suitable for this project/tests.
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

def hash_password(plain: str) -> str:
    return pwd_context.hash(plain)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)

def compute_result(op: str, a: float, b: float) -> float:
    if op == "add":       return a + b
    if op == "subtract":  return a - b
    if op == "multiply":  return a * b
    if op == "divide":
        if b == 0:
            raise ValueError("Division by zero")
        return a / b
    raise ValueError(f"Unknown operation: {op}")
