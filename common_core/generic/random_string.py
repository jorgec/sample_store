import string

import random


def generate_random_string(length: int = 64) -> str:
    generated_str = ''.join(random.choice(string.ascii_lowercase) for i in range(length))
    return generated_str
