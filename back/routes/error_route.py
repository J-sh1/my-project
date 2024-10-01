from fastapi import Request
from fastapi.responses import JSONResponse

# 404 에러 핸들러
async def page_not_found(request: Request, exc):
    return JSONResponse(status_code=404, content={"error": "Page not found"})

# 500 에러 핸들러
async def internal_server_error(request: Request, exc):
    return JSONResponse(status_code=500, content={"error": "Internal server error"})
