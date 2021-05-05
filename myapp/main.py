from fastapi import FastAPI

from .api.api import router as api_router
from mangum import Mangum

app = FastAPI(debug=True)

app.include_router(api_router, prefix="/v1")
handler = Mangum(app)