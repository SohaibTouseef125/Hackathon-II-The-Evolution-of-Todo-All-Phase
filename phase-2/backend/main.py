from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI(title="Todo API Phase-2", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://hackathon-ii-the-evolution-git-36d2ee-sohaib-touseefs-projects.vercel.app/","http://localhost:3000/"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Todo-App API "}

# Import and include routes
try:
    from routes import tasks, auth
    app.include_router(tasks.router, prefix="/api")
    app.include_router(auth.router, prefix="/api")
except (ImportError, ValueError):
    import sys
    import os
    # Add the project root to the path so imports work correctly
    project_root = os.path.dirname(os.path.abspath(__file__))
    if project_root not in sys.path:
        sys.path.insert(0, project_root)

    from routes import tasks, auth
    app.include_router(tasks.router, prefix="/api")
    app.include_router(auth.router, prefix="/api")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8001)))