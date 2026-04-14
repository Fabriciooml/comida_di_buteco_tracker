from pathlib import Path
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from api.routers import bars

app = FastAPI(title="Comida di Buteco")
app.include_router(bars.router, prefix="/api")

dist_dir = Path(__file__).parent.parent / "frontend" / "dist"
if dist_dir.exists():
    app.mount("/", StaticFiles(directory=str(dist_dir), html=True), name="static")
