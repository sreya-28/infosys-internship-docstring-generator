from fastapi import FastAPI, UploadFile, File, Form, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import ast
import os


app = FastAPI(title="Automated Python Docstring Generator")

# Get absolute paths for static and templates
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")

# Mount static files and templates using absolute paths
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
templates = Jinja2Templates(directory=TEMPLATES_DIR)

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

def validate_python_file(filename: str) -> bool:
    return filename and filename.lower().endswith('.py')

def extract_ast(code: str) -> str:
    try:
        tree = ast.parse(code)
        # Only return the AST as a string, no visualization or metrics
        return ast.dump(tree, indent=2)
    except SyntaxError as e:
        raise SyntaxError(f"Line {e.lineno}: {e.msg}")

@app.post("/analyze")
async def analyze_file(
    file: UploadFile = File(None),
    code_input: str = Form(None)
):
    try:
        content = None
        
        # Handle file upload
        if file and file.filename:
            if not validate_python_file(file.filename):
                return JSONResponse(
                    {"error": "❌ Please upload a Python (.py) file only!"}, 
                    status_code=400
                )
            content = await file.read()
            content = content.decode('utf-8')
        
        # Handle code input
        elif code_input and code_input.strip():
            content = code_input.strip()
        
        else:
            return JSONResponse(
                {"error": "❌ Please upload a file OR paste code!"}, 
                status_code=400
            )
        
        # Generate AST (string only, no visualization or metrics)
        ast_output = extract_ast(content)
        return {
            "success": True,
            "ast": ast_output,
            "message": "✅ AST generated successfully!"
        }
    except SyntaxError as e:
        return JSONResponse({"error": f"❌ Syntax Error: {str(e)}"}, status_code=400)
    except Exception as e:
        return JSONResponse({"error": f"❌ Error: {str(e)}"}, status_code=500)
