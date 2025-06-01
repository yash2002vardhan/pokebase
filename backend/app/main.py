from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from app.api.router import api_router
from app.config.logging import setup_logger
import time

logger = setup_logger("main")

app = FastAPI(
    title="Pokebase API",
    description="API for Pokebase application",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()

    logger.info(f"Request: {request.method} {request.url.path}")

    try:
        response = await call_next(request)
        process_time = time.time() - start_time
        logger.info(f"Response: {response.status_code} - Processed in {process_time:.2f}s")
        return response
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}", exc_info = True)
        raise
# Include the API router
app.include_router(api_router)
