"""固定场景，用来复现题面里的锚点。"""

import json

from . import core


def _line(obj):
    print(json.dumps(obj, ensure_ascii=False))


def acl(entries):
    return {"entries": entries}


def run(name):
    if name == "mask":
        a = acl([("user", "alice", "rwx"), ("mask", "", "r-x"), ("other", "", "---")])
        _line({"perms": core.evaluate(a, "alice", "bob", [], core.Counter())})
        return 0
    if name == "owner":
        a = acl([("user", "", "rwx"), ("mask", "", "r-x"), ("other", "", "---")])
        _line({"perms": core.evaluate(a, "alice", "alice", [], core.Counter())})
        return 0
    if name == "groupunion":
        a = acl([("group", "dev", "r--"), ("group", "ops", "-wx"),
                 ("mask", "", "rwx"), ("other", "", "---")])
        _line({"perms": core.evaluate(a, "alice", "bob", ["dev", "ops"], core.Counter())})
        return 0
    if name == "other":
        a = acl([("user", "alice", "rwx"), ("mask", "", "rwx"), ("other", "", "r--")])
        _line({"perms": core.evaluate(a, "carol", "bob", [], core.Counter())})
        return 0
    if name == "work":
        entries = [("user", "u%04d" % i, "rwx") for i in range(800)]
        entries.append(("mask", "", "rwx"))
        a = acl(entries)
        counter = core.Counter()
        for i in range(800):
            core.evaluate(a, "u%04d" % i, "bob", [], counter)
        _line({"entries": 800, "scanned": counter.scanned})
        return 0
    raise SystemExit("未知场景：" + name)
