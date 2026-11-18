# -*- coding: utf-8 -*-
"""mipstream"""

from __future__ import annotations

__all__ = ["MipChain", "Streamer", "request_level", "resident_set"]


class MipChain:
    """MipChain"""

    def __init__(self, base_bytes, levels):
        """mip 链"""
        raise NotImplementedError("MipChain.__init__ 尚未实现")

class Streamer:
    """Streamer"""

    def __init__(self, budget_bytes):
        """流送器"""
        raise NotImplementedError("Streamer.__init__ 尚未实现")


def request_level(streamer, texture_id, level):
    """请求某一级"""
    raise NotImplementedError("request_level 尚未实现")


def resident_set(streamer):
    """返回驻留集 {纹理: 级列表}"""
    raise NotImplementedError("resident_set 尚未实现")
