from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn
import os

# Create FastAPI app
app = FastAPI(title="Archon AI Legal Assistant")

# Mount static files directory
app.mount("/static", StaticFiles(directory="static"), name="static")

# Setup Jinja2 templates
templates = Jinja2Templates(directory="templates")

# Ensure directories exist
os.makedirs("static", exist_ok=True)
os.makedirs("static/css", exist_ok=True)
os.makedirs("static/js", exist_ok=True)
os.makedirs("templates", exist_ok=True)


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    """Serve the loading screen as the initial entry point"""
    return templates.TemplateResponse("loading.html", {"request": request})


@app.get("/app", response_class=HTMLResponse)
async def main_app(request: Request):
    """Serve the main application interface"""
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/health", response_class=HTMLResponse)
async def health_check():
    """Health check endpoint"""
    return HTMLResponse(content="OK", status_code=200)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
