import uvicorn
from app.main import app
from app.core.config import settings
if __name__ == "__main__":
    uvicorn.run(
        app="app.main:app",
        host=settings.SERVER_HOST,
        port=settings.SERVER_PORT,
        reload=False
    )
