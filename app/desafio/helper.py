import hashlib


def hashString(string):
    return hashlib.md5(string.encode()).hexdigest()
