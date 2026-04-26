from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import PlainTextResponse
from pydantic import BaseModel
from main import generate_imeis
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)
app = FastAPI(title="IMEI Generator API", version="0.1.0")
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


class GenerateRequest(BaseModel):
    prefix: str
    quantity: int = 50000

@app.post("/generate")
@limiter.limit("5/second")
def generate_imeis_endpoint(request: Request, payload: GenerateRequest):
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

@app.post("/generate/txt", response_class=PlainTextResponse)
@limiter.limit("5/second")
def generate_imeis_txt_endpoint(request: Request, payload: GenerateRequest):
    """Generate a list of IMEIs returning as plain text (one per line)."""
    if not payload.prefix.isdigit() or len(payload.prefix) != 8:
        raise HTTPException(status_code=400, detail="Prefix must be exactly 8 numeric digits.")
    if payload.quantity <= 0:
        raise HTTPException(status_code=400, detail="Quantity must be a positive integer.")
    
    imeis = generate_imeis(payload.prefix, payload.quantity)
    # Formata a lista para texto puro (um imei por linha)
    return "\n".join(imeis)
