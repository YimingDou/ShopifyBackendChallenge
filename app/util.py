import string

alphabet62 = string.ascii_letters + '0123456789'


def int_to_base62(n):
    base = 62
    s = []
    while n > 0:
        r = n % base
        n //= base
        s.append(alphabet62[r])
    s = s[::-1]
    return "".join(s)
