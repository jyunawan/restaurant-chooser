import random
import string


def generate_code():
    """
    Returns a 5 digit code consisting of lowercase letters, uppercase letters, and digits
    """
    return "".join(
        [random.choice(string.ascii_uppercase + string.digits) for _ in range(5)]
    )
