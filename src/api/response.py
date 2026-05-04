#/home/deb/my_project/maxbot_rebbit/src/api/response.py
from typing import Any


def success(data: Any = None):
    return {
        "success": True,
        "data": data or {}
    }


def ignored():
    return {
        "success": True,
        "ignored": True
    }


def error(code: str, message: str | None):
    return {
        "success": False,
        "error": {
            "code": code,
            "message": message
        }
    }

