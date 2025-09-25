
import os
import logging
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.responses import FileResponse
from fastapi.templating import Jinja2Templates
from fastapi import Request
from fastapi import UploadFile, File

class AppServer:
    def __init__(self):
        self.files_dir = "static/files"
        self.images_dir = "static/images"
        self.app = FastAPI()
        self.templates = Jinja2Templates(directory="app/templates")

        # Set up logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger("server")

        # Define routes
        self.setup_page_routes()
        self.setup_files_route()

    def setup_files_route(self):
        @self.app.get("/files/{filename}")
        async def get_file(filename: str):
            iso_dir = os.path.join(os.path.dirname(__file__), self.files_dir)
            file_path = os.path.join(iso_dir, filename)
            if not os.path.isfile(file_path):
                self.logger.warning(f"File not found: {file_path}")
                return {"error": "File not found"}
            self.logger.info(f"Serving file: {file_path}")
            return FileResponse(file_path, media_type="application/octet-stream", filename=filename)

        @self.app.post("/files/upload")
        async def upload_file(file: UploadFile = File(...)):
            iso_dir = os.path.join(os.path.dirname(__file__), self.files_dir)
            os.makedirs(iso_dir, exist_ok=True)
            file_path = os.path.join(iso_dir, file.filename)
            self.logger.info(f"Uploading file: {file_path}")
            with open(file_path, "wb") as f:
                while chunk := await file.read(1024 * 1024):
                    f.write(chunk)
            self.logger.info(f"Upload complete: {file_path}")
            return {"filename": file.filename, "status": "uploaded"}

    def setup_page_routes(self):
        @self.app.get("/", response_class=HTMLResponse)
        async def get_index(request: Request):
            return self.templates.TemplateResponse("index.html", {"request": request})

        @self.app.get("/images/favicon.png")
        async def get_favicon():
            favicon_path = os.path.join(os.path.dirname(__file__), f"{self.images_dir}/favicon-32x32.png")
            if os.path.isfile(favicon_path):
                return FileResponse(favicon_path, media_type="image/png")
            return {"error": "Favicon not found"}

# Create an instance of the AppServer class to run the app
app_server = AppServer()
app = app_server.app  # Expose the FastAPI app for running
