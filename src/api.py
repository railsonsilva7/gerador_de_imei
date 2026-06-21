import traceback
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import PlainTextResponse, JSONResponse
from pydantic import BaseModel
from main import generate_imeis

app = FastAPI(title="IMEI Generator API", version="0.1.0")

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"detail": str(exc), "traceback": traceback.format_exc()}
    )

class GenerateRequest(BaseModel):
    prefix: str
    quantity: int = 50000

@app.post("/generate")
def generate_imeis_endpoint(payload: GenerateRequest):
    """Generate a list of IMEIs.

    - **prefix**: 8‑digit numeric string (e.g., "35390744")
    - **quantity**: number of IMEIs to generate (default 50 000)
    """
    if not payload.prefix.isdigit() or len(payload.prefix) != 8:
        raise HTTPException(status_code=400, detail="Prefix must be exactly 8 numeric digits.")
    if payload.quantity <= 0:
        raise HTTPException(status_code=400, detail="Quantity must be a positive integer.")
    
    imeis = generate_imeis(payload.prefix, payload.quantity)
    return {"imeis": imeis}

@app.post("/generate/txt")
def generate_imeis_txt_endpoint(payload: GenerateRequest):
    """Generate a list of IMEIs and return as a downloadable .txt file."""
    if not payload.prefix.isdigit() or len(payload.prefix) != 8:
        raise HTTPException(status_code=400, detail="Prefix must be exactly 8 numeric digits.")
    if payload.quantity <= 0:
        raise HTTPException(status_code=400, detail="Quantity must be a positive integer.")

    imeis = generate_imeis(payload.prefix, payload.quantity)
    content = "\n".join(imeis)
    
    headers = {
        "Content-Disposition": 'attachment; filename="imeis.txt"'
    }
    return PlainTextResponse(content=content, headers=headers)

try:
    from workers import WorkerEntrypoint
    class Default(WorkerEntrypoint):
        async def fetch(self, request):
            import asgi
            return await asgi.fetch(app, request.js_object, self.env)
except ImportError:
    pass
