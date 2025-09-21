from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password : str) -> str:
    """
    Generates password hash
    """
    return pwd_context.hash(password)


def verify_password(password : str, hashed_password : str) -> bool:
    """
    Verify if plain password match with given hashed_password afte hashing it
    """
    return pwd_context.verify(password, hashed_password)

