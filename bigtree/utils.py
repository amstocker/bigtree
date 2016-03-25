import random
import string

ID_ALPHABET = string.digits + string.ascii_letters


def random_id():
    return ''.join(random.SystemRandom().choice(ID_ALPHABET)
                   for _ in range(8))
