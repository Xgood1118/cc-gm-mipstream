# -*- coding: utf-8 -*-
import argparse
import json
import mipstream as m


def main():
    ap = argparse.ArgumentParser(description="mipstream")
    ap.add_argument("path")
    ap.add_argument("--out", default=None)
    a = ap.parse_args()
    d = json.load(open(a.path, encoding="utf-8"))
    print(json.dumps({"textures": len(d["textures"])}, ensure_ascii=False))


if __name__ == "__main__":
    main()
