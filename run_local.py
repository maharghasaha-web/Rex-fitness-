import uvicorn
from app.db.database import init_db

if __name__ == "__main__":
    print("🚀 Initializing Local SQLite / PostgreSQL Schema...")
    init_db()
    print("✨ Starting FastAPI Backend Server on http://0.0.0.0:8000 ...")
    print("📱 iOS Simulator access:     http://127.0.0.1:8000/api/v1")
    print("🤖 Android Emulator access:  http://10.0.2.2:8000/api/v1")
    print("📚 OpenAPI Swagger UI:       http://127.0.0.1:8000/docs")
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
