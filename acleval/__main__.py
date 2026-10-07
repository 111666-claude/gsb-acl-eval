"""命令行入口。"""

import argparse

from . import samples


def main(argv=None):
    ap = argparse.ArgumentParser(prog="acleval")
    ap.add_argument("--sample", choices=["mask", "owner", "groupunion", "other", "work"])
    args = ap.parse_args(argv)
    if args.sample:
        return samples.run(args.sample)
    ap.print_help()
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
