import logging
import sys
import traceback
from fastapi import FastAPI, Request, File, UploadFile, Form, WebSocket, BackgroundTasks
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Union, Dict, Any
import uvicorn
import os
import asyncio
import io
import json
import tempfile
from datetime import datetime
import shutil

# Setup logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger("archon")

# Import your agent modules
try:
    logger.info("Importing agent modules...")
    from archonAgents.legalAnalysis import legalAnalysisAG
    from archonAgents.documentReview import documentReviewAG
    from archonAgents.caseEvaluation import caseEvaluationAG
    from archonAgents.mcpAgents import mcpAgent
    from archonAgents.legalClock import legalClock

    logger.info("Successfully imported agent modules")
except Exception as e:
    logger.error(f"Error importing agent modules: {str(e)}")
    logger.error(traceback.format_exc())
    raise

# Create FastAPI app
app = FastAPI(title="Archon AI Legal Assistant")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files directory
app.mount("/static", StaticFiles(directory="static"), name="static")

# Setup Jinja2 templates
templates = Jinja2Templates(directory="templates")

# Ensure directories exist
os.makedirs("static", exist_ok=True)
os.makedirs("static/css", exist_ok=True)
os.makedirs("static/js", exist_ok=True)
os.makedirs("static/img", exist_ok=True)
os.makedirs("templates", exist_ok=True)
os.makedirs("uploads", exist_ok=True)  # Create upload directory


# Define request models
class ChatRequest(BaseModel):
    message: str
    tool: str


class FileUploadRequest(BaseModel):
    message: str = Form(...)
    tool: str = Form(...)
    files: List[UploadFile] = File(None)


# Active WebSocket connections
active_connections: Dict[str, WebSocket] = {}


# Helper functions
async def process_file(file: UploadFile) -> str:
    """Process uploaded file and return its content as text"""
    logger.info(f"Processing file: {file.filename}")
    content = await file.read()

    # Create a temp file to handle non-text formats properly
    suffix = os.path.splitext(file.filename)[1]
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_file:
        temp_file.write(content)
        temp_path = temp_file.name

    # Read file content based on type
    file_content = ""

    if suffix.lower() == ".txt":
        logger.info("Processing as TXT file")
        with open(temp_path, "r", encoding="utf-8") as f:
            file_content = f.read()

    elif suffix.lower() == ".pdf":
        logger.info("Processing as PDF file")
        try:
            import PyPDF2

            with open(temp_path, "rb") as f:
                pdf_reader = PyPDF2.PdfReader(f)
                file_content = ""
                for page_num in range(len(pdf_reader.pages)):
                    file_content += pdf_reader.pages[page_num].extract_text() + "\n"
        except ImportError:
            file_content = "Error: PyPDF2 module not found."
            logger.error("PyPDF2 module not found")

    elif suffix.lower() in [".doc", ".docx"]:
        logger.info("Processing as DOCX file")
        try:
            import docx

            doc = docx.Document(temp_path)
            file_content = "\n".join([para.text for para in doc.paragraphs])
        except ImportError:
            file_content = "Error: python-docx module not found."
            logger.error("python-docx module not found")

    # Clean up temp file
    os.unlink(temp_path)
    logger.info(f"Finished processing file: {file.filename}")

    return file_content


async def save_file(file: UploadFile) -> str:
    """Save uploaded file and return the saved path"""
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f"{timestamp}_{file.filename}"
    file_path = os.path.join("uploads", filename)

    # Ensure uploads directory exists
    os.makedirs("uploads", exist_ok=True)

    # Save the file
    content = await file.read()
    with open(file_path, "wb") as f:
        f.write(content)

    # Reset file position to beginning for future reads
    await file.seek(0)

    return file_path


# Routes
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


# API Endpoints
@app.post("/api/chat")
async def chat(request: ChatRequest):
    """
    General chat endpoint without file uploads
    """
    logger.info(
        f"Chat request received - Tool: '{request.tool}', Message length: {len(request.message)}"
    )
    try:
        response = ""
        # Normalize tool name to handle various formats
        tool_original = request.tool
        tool = request.tool.lower().strip()

        logger.debug(f"Normalized tool name: '{tool}'")

        if tool == "legal analysis":
            logger.info("Calling Legal Analysis agent")
            response = legalAnalysisAG(request.message)
            logger.info("Legal Analysis agent returned response")
        elif tool == "document review":
            logger.info("Calling Document Review agent")
            response = documentReviewAG(request.message)
            logger.info("Document Review agent returned response")
        elif tool == "case evaluation":
            logger.info("Calling Case Evaluation agent")
            response = caseEvaluationAG(request.message)
            logger.info("Case Evaluation agent returned response")
        elif tool == "legal clock":
            logger.info("Calling Legal Clock agent")
            response = legalClock(request.message)
            logger.info("Legal Clock agent returned response")
        elif tool in ["quick summary", "quick summary (experimental)"]:
            logger.info("Calling Quick Summary (MCP) agent")
            try:
                # Debug information about the mcpAgent function
                logger.debug(f"mcpAgent function: {mcpAgent}")
                logger.debug(
                    f"mcpAgent expects args: {mcpAgent.__code__.co_varnames[: mcpAgent.__code__.co_argcount]}"
                )

                # Call the MCP agent and await its response
                response = await mcpAgent(request.message)
                logger.info("Quick Summary agent returned response")
            except Exception as mcp_error:
                logger.error(f"Error in mcpAgent: {str(mcp_error)}")
                logger.error(traceback.format_exc())
                return JSONResponse(
                    status_code=500,
                    content={"error": f"MCP Agent error: {str(mcp_error)}"},
                )
        elif tool == "legal clock":
            logger.info("Calling Legal Clock agent")
            response = legalClock(request.message)
            logger.info("Legal Clock agent returned response")
        else:
            logger.warning(f"Unknown tool requested: '{tool_original}'")
            return JSONResponse(
                status_code=400, content={"error": f"Unknown tool: {tool_original}"}
            )

        logger.info(f"Returning successful response from {tool_original}")
        return {"response": response}

    except Exception as e:
        logger.error(f"Error in chat endpoint: {str(e)}")
        logger.error(traceback.format_exc())
        return JSONResponse(
            status_code=500, content={"error": f"An error occurred: {str(e)}"}
        )


@app.post("/api/upload")
async def upload_file(
    message: str = Form(...),
    tool: str = Form(...),
    files: List[UploadFile] = File(None),
):
    """
    Endpoint for chat with file uploads
    """
    logger.info(
        f"Upload request received - Tool: '{tool}', Message length: {len(message)}, Files: {len(files) if files else 0}"
    )
    try:
        # Process files if any
        file_contents = []
        if files:
            for file in files:
                if file.filename:  # Skip empty file entries
                    logger.info(f"Processing file: {file.filename}")
                    content = await process_file(file)
                    file_contents.append(content)

        # Combine file contents
        combined_content = "\n\n".join(file_contents) if file_contents else None

        # Call appropriate agent based on tool
        response = ""
        tool_lower = tool.lower().strip()

        logger.debug(f"Normalized tool name: '{tool_lower}'")

        if tool_lower == "legal analysis":
            logger.info("Calling Legal Analysis agent with file content")
            response = legalAnalysisAG(message, combined_content)
            logger.info("Legal Analysis agent returned response")
        elif tool_lower == "document review":
            logger.info("Calling Document Review agent with file content")
            response = documentReviewAG(message, combined_content)
            logger.info("Document Review agent returned response")
        elif tool_lower == "case evaluation":
            logger.info("Calling Case Evaluation agent with file content")
            response = caseEvaluationAG(message, combined_content)
            logger.info("Case Evaluation agent returned response")
        elif tool_lower in ["quick summary", "quick summary (experimental)"]:
            logger.info("Calling Quick Summary (MCP) agent with file content")
            try:
                # For MCP Agent, we need to enhance the prompt with file content
                if combined_content:
                    enhanced_prompt = (
                        f"File Content:\n{combined_content}\n\nUser Query:\n{message}"
                    )
                    logger.debug("Created enhanced prompt with file content")
                else:
                    enhanced_prompt = message
                    logger.debug("Using original message as prompt (no file content)")

                response = await mcpAgent(enhanced_prompt)
                logger.info("Quick Summary agent returned response")
            except Exception as mcp_error:
                logger.error(f"Error in mcpAgent with file: {str(mcp_error)}")
                logger.error(traceback.format_exc())
                return JSONResponse(
                    status_code=500,
                    content={"error": f"MCP Agent error: {str(mcp_error)}"},
                )
        elif tool_lower == "legal clock":
            logger.info("Calling Legal Clock agent")
            response = legalClock(message)
            logger.info("Legal Clock agent returned response")
        else:
            logger.warning(f"Unknown tool requested in upload: '{tool}'")
            return JSONResponse(
                status_code=400, content={"error": f"Unknown tool: {tool}"}
            )

        logger.info(f"Returning successful response from {tool} (upload endpoint)")
        return {"response": response}

    except Exception as e:
        logger.error(f"Error in upload endpoint: {str(e)}")
        logger.error(traceback.format_exc())
        return JSONResponse(
            status_code=500, content={"error": f"An error occurred: {str(e)}"}
        )


# WebSocket for real-time streaming (optional enhancement)
@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    logger.info(f"WebSocket connection attempt from client {client_id}")
    await websocket.accept()
    active_connections[client_id] = websocket
    logger.info(f"WebSocket connection accepted for client {client_id}")

    try:
        while True:
            data = await websocket.receive_text()
            logger.info(f"WebSocket message received from client {client_id}")

            # Process the message
            try:
                request_data = json.loads(data)
                message = request_data.get("message", "")
                tool = request_data.get("tool", "").lower().strip()

                logger.info(
                    f"WebSocket - Tool: '{tool}', Message length: {len(message)}"
                )

                # Call the appropriate agent
                if tool == "legal analysis":
                    logger.info("WebSocket - Calling Legal Analysis agent")
                    response = legalAnalysisAG(message)
                    logger.info("WebSocket - Legal Analysis agent returned response")
                elif tool == "document review":
                    logger.info("WebSocket - Calling Document Review agent")
                    response = documentReviewAG(message)
                    logger.info("WebSocket - Document Review agent returned response")
                elif tool == "case evaluation":
                    logger.info("WebSocket - Calling Case Evaluation agent")
                    response = caseEvaluationAG(message)
                    logger.info("WebSocket - Case Evaluation agent returned response")
                elif tool in ["quick summary", "quick summary (experimental)"]:
                    logger.info("WebSocket - Calling Quick Summary (MCP) agent")
                    try:
                        response = await mcpAgent(message)
                        logger.info("WebSocket - Quick Summary agent returned response")
                    except Exception as mcp_error:
                        logger.error(f"WebSocket - Error in mcpAgent: {str(mcp_error)}")
                        response = f"Error in MCP Agent: {str(mcp_error)}"
                elif tool == "legal clock":
                    logger.info("WebSocket - Calling Legal Clock agent")
                    response = legalClock(message)
                    logger.info("WebSocket - Legal Clock agent returned response")
                else:
                    logger.warning(f"WebSocket - Unknown tool requested: '{tool}'")
                    response = f"Unknown tool: {tool}"

                # Send response back to client
                await websocket.send_text(json.dumps({"response": response}))
                logger.info(f"WebSocket - Response sent to client {client_id}")

            except Exception as e:
                logger.error(f"WebSocket - Error processing message: {str(e)}")
                logger.error(traceback.format_exc())
                await websocket.send_text(json.dumps({"error": str(e)}))
                logger.info(f"WebSocket - Error message sent to client {client_id}")

    except Exception as e:
        logger.error(f"WebSocket - Connection error: {str(e)}")
        # Client disconnected

    finally:
        if client_id in active_connections:
            logger.info(
                f"WebSocket - Removing client {client_id} from active connections"
            )
            del active_connections[client_id]


if __name__ == "__main__":
    logger.info("Starting Archon AI Legal Assistant server")
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
