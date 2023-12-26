import hashlib
import json


class CallableValue(object):
    def __init__(self, value):
        self.value = value

    def __call__(self, *args, **kwargs):
        return self.value


def do_pbkdf2_not_coded(to_hash: str, salt: str) -> str:
    return hashlib.pbkdf2_hmac("sha256", to_hash.encode(), salt.encode(), 1000, 128).hex()[:32]


is_first = True


def pretty_print(arg):
    if isinstance(arg, dict):
        arg = json.dumps(arg, indent=4, )
    separator = "========================================="
    global is_first
    if is_first:
        is_first = False
        print(separator)
    print(arg)
    print(separator)
