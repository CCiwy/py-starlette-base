from datetime import datetime

import random
import uuid


def generate_seed(base_str: str) -> int:
    now = datetime.now()
    dated_str = f'{base_str}_{now}'
    seed = int(''.join(map(str, map(ord, dated_str))))
    return seed


def get_uuid(seed_str: str) -> str:

    seed = generate_seed(seed_str)
    rng = random.Random()
    rng.seed(seed)

    _uuid = str(uuid.UUID(int=rng.getrandbits(128), version=4).hex)
    return _uuid
