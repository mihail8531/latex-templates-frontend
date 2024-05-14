import json
from fastapi import HTTPException, status


def hx_location(path: str, target: str | None = None) -> dict[str, str]:
    """
    Create hx location header
    """
    if target is None:
        hx_location_value = path
    else:
        hx_location_value = json.dumps({"path": path, "target": target})
    return {"HX-Location": hx_location_value, "HX-Replace-Url": "/"}

