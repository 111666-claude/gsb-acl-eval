"""求值 POSIX ACL。"""


class Counter:
    """记录比较次数。"""

    def __init__(self):
        self.scanned = 0


def _to_bits(text):
    bits = 0
    if "r" in text:
        bits |= 4
    if "w" in text:
        bits |= 2
    if "x" in text:
        bits |= 1
    return bits


def _to_text(bits):
    return ("r" if bits & 4 else "-") + ("w" if bits & 2 else "-") + ("x" if bits & 1 else "-")


def evaluate(acl, uid, owner, groups, counter):
    entries = acl.get("entries", [])
    mask = 7
    for kind, qualifier, perms in entries:
        counter.scanned += 1
        if kind == "mask":
            mask = _to_bits(perms)
    for kind, qualifier, perms in entries:
        counter.scanned += 1
        if kind == "user" and qualifier == "" and uid == owner:
            return _to_text(_to_bits(perms) & mask)
    for kind, qualifier, perms in entries:
        counter.scanned += 1
        if kind == "user" and qualifier == uid:
            return _to_text(_to_bits(perms))
    for kind, qualifier, perms in entries:
        counter.scanned += 1
        if kind == "group" and qualifier in groups:
            return _to_text(_to_bits(perms) & mask)
    return "---"
