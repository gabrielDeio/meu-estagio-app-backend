import random
import string

def generate(size: int = 6) -> str:
    """
    Generate an organization enrollment code.
    """
    
    characteres = string.ascii_uppercase + string.digits
    
    code = ''.join(random.choice(characteres) for _ in range(size))
    
    return code
