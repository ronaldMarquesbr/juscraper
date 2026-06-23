import random
import time


def bool_to_str(value):
    return str(value).lower()


def sleep_random(min_seconds=3, max_seconds=8):
    time.sleep(random.uniform(min_seconds, max_seconds))
