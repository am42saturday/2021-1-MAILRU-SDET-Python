import random
import string


def generate_random_name(length):
    result = ''.join(random.choice(string.ascii_letters) for _ in range(length))
    return result
