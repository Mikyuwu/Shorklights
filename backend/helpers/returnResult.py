from fastapi.responses import JSONResponse
from typing import Any, Optional

def return_result(
    success: bool,
    message: Optional[str] = None,
    type: Optional[str] = None,
    data: Optional[Any] = None,
    status_code: int = 200
) -> JSONResponse:
    payload = {"success": success}
    if message is not None:
        payload["message"] = message
    if type is not None:
        payload["type"] = type
    if data is not None:
        payload["data"] = data
    return JSONResponse(status_code=status_code, content=payload)