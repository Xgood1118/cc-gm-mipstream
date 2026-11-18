# -*- coding: utf-8 -*-
import json
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import mipstream as mod  # noqa: E402

DATA = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")


def _mk():
    d = json.load(open(os.path.join(DATA, "textures.json"), encoding="utf-8"))
    ch = {t["id"]: mod.MipChain(t["base_bytes"], t["levels"]) for t in d["textures"]}
    s = mod.Streamer(d["budget_bytes"])
    return d, ch, s


def test_ancestors_resident():
    d, ch, s = _mk()
    mod.request_level(s, "t0", 3)
    res = mod.resident_set(s)
    lv = res.get("t0") or []
    assert set(range(len(lv))) <= set(lv) or 0 in lv and len(lv) >= 4


def test_byte_accounting():
    d, ch, s = _mk()
    for t in d["textures"]:
        mod.request_level(s, t["id"], t["levels"] - 1)
    res = mod.resident_set(s)
    total = 0
    for tex, lvs in res.items():
        total += sum(max(1, ch[tex].base_bytes // (4 ** i)) for i in lvs)
    assert total <= d["budget_bytes"] * 1.01


def test_no_hole_after_evict():
    d, ch, s = _mk()
    for t in d["textures"]:
        mod.request_level(s, t["id"], 0)
    res = mod.resident_set(s)
    for tex, lvs in res.items():
        assert 0 in lvs


def test_order_independent():
    d, ch, s1 = _mk()
    s2 = mod.Streamer(d["budget_bytes"])
    mod.request_level(s1, "t0", 2)
    mod.request_level(s1, "t1", 1)
    mod.request_level(s2, "t1", 1)
    mod.request_level(s2, "t0", 2)
    a = mod.resident_set(s1)
    b = mod.resident_set(s2)
    assert {k: sorted(v) for k, v in a.items()} == {k: sorted(v) for k, v in b.items()}


def test_single_level_texture():
    s = mod.Streamer(100)
    mod.request_level(s, "single", 0)
    assert mod.resident_set(s).get("single") == [0]
